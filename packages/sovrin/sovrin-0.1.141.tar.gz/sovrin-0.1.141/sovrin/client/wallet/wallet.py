import datetime
import json
import operator
import uuid
from collections import deque
from typing import Dict
from typing import Optional

from anoncreds.protocol.utils import strToCryptoInteger
from ledger.util import F
from plenum.client.wallet import Wallet as PWallet
from plenum.common.did_method import DidMethods
from plenum.common.log import getlogger
from plenum.common.txn import TXN_TYPE, TARGET_NYM, DATA, \
    IDENTIFIER, NAME, VERSION, TYPE, NYM, ROLE, ORIGIN
from plenum.common.types import Identifier, f
from sovrin.client.wallet.attribute import Attribute, AttributeKey
from sovrin.client.wallet.claim_def import ClaimDef, IssuerPubKey
from sovrin.client.wallet.issuer_wallet import IssuerWallet
from sovrin.client.wallet.link import Link
from sovrin.client.wallet.prover_wallet import ProverWallet
from sovrin.client.wallet.sponsoring import Sponsoring
from sovrin.common.did_method import DefaultDidMethods
from sovrin.common.exceptions import LinkNotFound
from sovrin.common.identity import Identity
from sovrin.common.txn import ATTRIB, GET_TXNS, GET_ATTR, CRED_DEF, \
    GET_CRED_DEF, \
    GET_NYM, ATTR_NAMES, ISSUER_KEY, GET_ISSUER_KEY, REF
from sovrin.common.util import stringDictToCharmDict

ENCODING = "utf-8"

logger = getlogger()


# TODO: Maybe we should have a thinner wallet which should not have ProverWallet
class Wallet(PWallet, Sponsoring, ProverWallet, IssuerWallet):
    clientNotPresentMsg = "The wallet does not have a client associated with it"

    def __init__(self,
                 name: str,
                 supportedDidMethods: DidMethods=None,
                 defaultClaimType=None):
        PWallet.__init__(self,
                         name,
                         supportedDidMethods or DefaultDidMethods)
        Sponsoring.__init__(self)
        ProverWallet.__init__(self)
        IssuerWallet.__init__(self, defaultClaimType or 'CL')
        self._attributes = {}  # type: Dict[(str, Identifier,
        # Optional[Identifier]), Attribute]
        self._claimDefs = {}  # type: Dict[(str, str, str), ClaimDef]
        self._claimDefSks = {}  # type: Dict[(str, str, str), ClaimDefSk]

        self._links = {}  # type: Dict[str, Link]
        self.knownIds = {}  # type: Dict[str, Identifier]

        # TODO: Shouldnt proof builders be uniquely identified by claim def
        # and issuerId
        # TODO: Create claim objects

        self._issuerSks = {}
        self._issuerPks = {}
        # transactions not yet submitted
        self._pending = deque()  # type Tuple[Request, Tuple[str, Identifier,
        #  Optional[Identifier]]

        # pending transactions that have been prepared (probably submitted)
        self._prepared = {}  # type: Dict[(Identifier, int), Request]
        self.lastKnownSeqs = {}  # type: Dict[str, int]

        self.replyHandler = {
            ATTRIB: self._attribReply,
            GET_ATTR: self._getAttrReply,
            CRED_DEF: self._claimDefReply,
            GET_CRED_DEF: self._getClaimDefReply,
            NYM: self._nymReply,
            GET_NYM: self._getNymReply,
            GET_TXNS: self._getTxnsReply,
            ISSUER_KEY: self._issuerKeyReply,
            GET_ISSUER_KEY: self._getIssuerKeyReply,
        }

    @property
    def pendingCount(self):
        return len(self._pending)

    @staticmethod
    def _isMatchingName(needle, haystack):
        return needle.lower() in haystack.lower()

    def getClaimAttrs(self, claimDefKey) -> Dict:
        # TODO: The issuer can be different than the author of the claim
        # definition. But assuming that issuer is the author of the claim
        # definition for now
        issuerId = claimDefKey[2]
        claimDef = self.getClaimDef(key=claimDefKey)
        if claimDef and claimDef.attrNames and issuerId in self.attributesFrom:
            return {nm: self.attributesFrom[issuerId].get(nm) for nm
                    in claimDef.attrNames}
        return {}

    def getMatchingRcvdClaims(self, attributes):
        matchingLinkAndRcvdClaim = []
        matched = set()
        attrNames = set(attributes.keys())
        for li in self._links.values():
            issuedAttributes = self.attributesFrom.get(li.remoteIdentifier)
            if issuedAttributes:
                commonAttrs = (attrNames.difference(matched).intersection(
                    set(issuedAttributes.keys())))
                if commonAttrs:
                    for nm, ver, origin in li.availableClaims:
                        cd = self.getClaimDef(key=(nm, ver, origin))
                        if cd and cd.seqNo and set(cd.attrNames).intersection(
                                commonAttrs):
                            matchingLinkAndRcvdClaim.append((li,
                                                             (nm, ver, origin),
                                                             commonAttrs,
                                                             issuedAttributes))
                            matched.update(commonAttrs)
                            break
        return matchingLinkAndRcvdClaim

    # TODO: The names getMatchingLinksWithAvailableClaim and
    # getMatchingLinksWithReceivedClaim should be fixed. Difference between
    # `AvailableClaim` and `ReceivedClaim` is that for ReceivedClaim we
    # have attribute values from issuer.

    # TODO: Few of the below methods have duplicate code, need to refactor it
    def getMatchingLinksWithAvailableClaim(self, claimName):
        matchingLinkAndAvailableClaim = []
        for k, li in self._links.items():
            for cl in li.availableClaims:
                if Wallet._isMatchingName(claimName, cl[0]):
                    matchingLinkAndAvailableClaim.append((li, cl))
        return matchingLinkAndAvailableClaim

    def getMatchingLinksWithReceivedClaim(self, claimName):
        matchingLinkAndReceivedClaim = []
        for k, li in self._links.items():
            for cl in li.availableClaims:
                if Wallet._isMatchingName(claimName, cl[0]):
                    claimDef = self.getClaimDef(key=cl)
                    issuedAttributes = self.attributesFrom.get(
                        li.remoteIdentifier)
                    if issuedAttributes:
                        claimAttrs = set(claimDef.attrNames)
                        if claimAttrs.intersection(issuedAttributes.keys()):
                            matchingLinkAndReceivedClaim.append(
                                (li, cl, {k: issuedAttributes[k] for k in
                                          claimAttrs}))
        return matchingLinkAndReceivedClaim

    def getMatchingLinksWithClaimReq(self, claimReqName, linkName=None):
        matchingLinkAndClaimReq = []
        for k, li in self._links.items():
            for cpr in li.claimProofRequests:
                if Wallet._isMatchingName(claimReqName, cpr.name):
                    if linkName is None or Wallet._isMatchingName(linkName,
                                                                  li.name):
                        matchingLinkAndClaimReq.append((li, cpr))
        return matchingLinkAndClaimReq

    def addAttribute(self, attrib: Attribute):
        """
        Used to create a new attribute on Sovrin
        :param attrib: attribute to add
        :return: number of pending txns
        """
        self._attributes[attrib.key()] = attrib
        req = attrib.ledgerRequest()
        if req:
            self.pendRequest(req, attrib.key())
        return len(self._pending)

    def hasAttribute(self, key: AttributeKey) -> bool:
        """
        Checks if attribute is present in the wallet
        @param name: Name of the attribute
        @return:
        """
        return bool(self.getAttribute(key))

    def getAttribute(self, key: AttributeKey):
        return self._attributes.get(key.key())

    def getAttributesForNym(self, idr: Identifier):
        return [a for a in self._attributes.values() if a.dest == idr]

    def addAttrFrom(self, frm, attrs):
        assert isinstance(attrs, dict)
        if frm not in self.attributesFrom:
            self.attributesFrom[frm] = {}
        self.attributesFrom[frm].update(attrs)

    def addClaimDef(self, claimDef: ClaimDef):
        """
        Used to create a new cred def on Sovrin
        :param claimDef: claimDef to add
        :return: number of pending txns
        """
        self._claimDefs[claimDef.key] = claimDef
        req = claimDef.request
        if req:
            self.pendRequest(req, claimDef.key)
        return len(self._pending)

    def getClaimDef(self, key=None, seqNo=None):
        assert key or seqNo
        if key:
            return self._claimDefs.get(key)
        else:
            for _, cd in self._claimDefs.items():
                if cd.seqNo == seqNo:
                    return cd

    def addLink(self, link: Link):
        self._links[link.key] = link

    def getLink(self, name, required=False) -> Link:
        l = self._links.get(name)
        if not l and required:
            logger.debug("Wallet has links {}".format(self._links))
            raise LinkNotFound(l.name)
        return l

    def addLastKnownSeqs(self, identifier, seqNo):
        self.lastKnownSeqs[identifier] = seqNo

    def getLastKnownSeqs(self, identifier):
        return self.lastKnownSeqs.get(identifier)

    def getPendingTxnRequests(self, *identifiers):
        if not identifiers:
            identifiers = self.idsToSigners.keys()
        else:
            identifiers = set(identifiers).intersection(
                set(self.idsToSigners.keys()))
        requests = []
        for identifier in identifiers:
            lastTxn = self.getLastKnownSeqs(identifier)
            op = {
                TARGET_NYM: identifier,
                TXN_TYPE: GET_TXNS,
            }
            if lastTxn:
                op[DATA] = lastTxn
            requests.append(self.signOp(op, identifier=identifier))
        return requests

    def pendSyncRequests(self):
        pendingTxnsReqs = self.getPendingTxnRequests()
        for req in pendingTxnsReqs:
            self.pendRequest(req)

    def preparePending(self):
        new = {}
        while self._pending:
            req, key = self._pending.pop()
            sreq = self.signRequest(req)
            new[req.identifier, req.reqId] = sreq, key
        self._prepared.update(new)
        # Return request in the order they were submitted
        return sorted([req for req, _ in new.values()],
                      key=operator.attrgetter("reqId"))

    def handleIncomingReply(self, observer_name, reqId, frm, result,
                            numReplies):
        """
        Called by an external entity, like a Client, to notify of incoming
        replies
        :return:
        """
        preparedReq = self._prepared.get((result[IDENTIFIER], reqId))
        if not preparedReq:
            raise RuntimeError('no matching prepared value for {},{}'.
                               format(result[IDENTIFIER], reqId))
        typ = result.get(TXN_TYPE)
        if typ and typ in self.replyHandler:
            self.replyHandler[typ](result, preparedReq)
        else:
            raise NotImplementedError('No handler for {}'.format(typ))

    def _attribReply(self, result, preparedReq):
        _, attrKey = preparedReq
        attrib = self.getAttribute(AttributeKey(*attrKey))
        attrib.seqNo = result[F.seqNo.name]

    def _getAttrReply(self, result, preparedReq):
        # TODO: Confirm if we need to add the retrieved attribute to the wallet.
        # If yes then change the graph query on node to return the sequence
        # number of the attribute txn too.
        _, attrKey = preparedReq
        attrib = self.getAttribute(AttributeKey(*attrKey))
        if DATA in result:
            attrib.value = result[DATA]
            attrib.seqNo = result[F.seqNo.name]
        else:
            logger.debug("No attribute found")

    def _claimDefReply(self, result, preparedReq):
        # TODO: Duplicate code from _attribReply, abstract this behavior,
        # Have a mixin like `HasSeqNo`
        _, key = preparedReq
        claimDef = self.getClaimDef(key)
        claimDef.seqNo = result[F.seqNo.name]

    def _getClaimDefReply(self, result, preparedReq):
        data = json.loads(result.get(DATA))
        if data:
            claimDef = self.getClaimDef((data.get(NAME), data.get(VERSION),
                                         data.get(ORIGIN)))
            if claimDef:
                if not claimDef.seqNo:
                    claimDef.seqNo = data.get(F.seqNo.name)
                    claimDef.attrNames = data[ATTR_NAMES].split(",")
                    claimDef.typ = data[TYPE]
            else:
                claimDef = ClaimDef(seqNo=data.get(F.seqNo.name),
                                    attrNames=data.get(ATTR_NAMES).split(","),
                                    name=data[NAME],
                                    version=data[VERSION],
                                    origin=data[ORIGIN],
                                    typ=data[TYPE])
                self._claimDefs[claimDef.key] = claimDef
        else:
            logger.info("Requested claim def was not found on the ledger")

    def _nymReply(self, result, preparedReq):
        target = result[TARGET_NYM]
        idy = self._sponsored.get(target)
        if idy:
            idy.seqNo = result[F.seqNo.name]
        else:
            logger.error("Target {} not found in sponsored".format(target))
            raise NotImplementedError

    def _getNymReply(self, result, preparedReq):
        jsonData = result.get(DATA)
        if jsonData:
            data = json.loads(jsonData)
            nym = data.get(TARGET_NYM)
            idy = self.knownIds.get(nym)
            if idy:
                idy.role = data.get(ROLE)
                idy.sponsor = data.get(f.IDENTIFIER.nm)
                idy.last_synced = datetime.datetime.utcnow()
                # TODO: THE GET_NYM reply should contain the sequence number of
                # the NYM transaction
        else:
            raise NotImplementedError("'DATA' in reply was None")

    def _getTxnsReply(self, result, preparedReq):
        # TODO
        pass

    def _issuerKeyReply(self, result, preparedReq):
        data = result.get(DATA)
        ref = result.get(REF)
        key = self._getMatchingIssuerKey(data)
        if key and self._issuerPks[key].claimDefSeqNo == ref:
            self._issuerPks[key].seqNo = result.get(F.seqNo.name)
            return self._issuerPks[key].seqNo
        else:
            raise Exception("Not found appropriate issuer key to update")

    def _getIssuerKeyReply(self, result, preparedReq):
        data = json.loads(result.get(DATA))
        if data:
            key = data.get(ORIGIN), data.get(REF)
            isPk = self.getIssuerPublicKey(key=key)
            keys = data.get(DATA)
            for k in ('N', 'S', 'Z'):
                keys[k] = strToCryptoInteger(keys[k])
            keys['R'] = stringDictToCharmDict(keys['R'])
            isPk.initPubKey(data.get(F.seqNo.name), keys['N'], keys['R'],
                            keys['S'], keys['Z'])
        else:
            logger.info("Requested issuer key was not found on the ledger")

    def _getMatchingIssuerKey(self, data):
        for key, pk in self._issuerPks.items():
            if str(pk.N) == data.get("N") and str(pk.S) == data.get("S") and \
                            str(pk.Z) == data.get("Z"):
                matches = 0
                for k, v in pk.R.items():
                    if str(pk.R.get(k)) == data.get("R").get(k):
                        matches += 1
                    else:
                        break
                if matches == len(pk.R):
                    return key
        return None

    def pendRequest(self, req, key=None):
        self._pending.appendleft((req, key))

    def getLinkInvitationByTarget(self, target: str) -> Link:
        for k, li in self._links.items():
            if li.remoteIdentifier == target:
                return li

    def getLinkInvitation(self, name: str):
        return self._links.get(name)

    def getMatchingLinks(self, name: str):
        allMatched = []
        for k, v in self._links.items():
            if self._isMatchingName(name, k):
                allMatched.append(v)
        return allMatched

    # TODO: sender by default should be `self.defaultId`
    def requestAttribute(self, attrib: Attribute, sender):
        """
        Used to get a raw attribute from Sovrin
        :param attrib: attribute to add
        :return: number of pending txns
        """
        self._attributes[attrib.key()] = attrib
        req = attrib.getRequest(sender)
        if req:
            return self.prepReq(req, key=attrib.key())

    # TODO: sender by default should be `self.defaultId`
    def requestIdentity(self, identity: Identity, sender):
        # Used to get a nym from Sovrin
        self.knownIds[identity.identifier] = identity
        req = identity.getRequest(sender)
        if req:
            return self.prepReq(req)

    # TODO: sender by default should be `self.defaultId`
    def requestClaimDef(self, claimDefKey, sender):
        # Used to get a cred def from Sovrin
        name, version, origin = claimDefKey
        claimDef = ClaimDef(name=name, version=version, origin=origin)
        self._claimDefs[claimDefKey] = claimDef
        req = claimDef.getRequest(sender)
        if req:
            return self.prepReq(req)

    # TODO: sender by default should be `self.defaultId`
    def requestIssuerKey(self, issuerKey, sender):
        # Used to get a issuer key from Sovrin
        origin, claimDefSeqNo = issuerKey
        isPk = IssuerPubKey(origin=origin, claimDefSeqNo=claimDefSeqNo)
        self._issuerPks[issuerKey] = isPk
        req = isPk.getRequest(sender)
        if req:
            return self.prepReq(req)

    def prepReq(self, req, key=None):
        self.pendRequest(req, key=key)
        return self.preparePending()[0]

    # DEPR
    # def getLinkByNonce(self, nonce) -> Optional[Link]:
    #     for _, li in self._links.items():
    #         if li.nonce == nonce:
    #             return li

    def getLinkByInternalId(self, internalId) -> Optional[Link]:
        for _, li in self._links.items():
            if li.internalId == internalId:
                return li

    def addIssuerSecretKey(self, issuerSk):
        self._issuerSks[issuerSk.pubkey.uid] = issuerSk
        return issuerSk.pubkey.uid

    def getIssuerSecretKey(self, uid):
        return self._issuerSks.get(uid)

    def addIssuerPublicKey(self, issuerPk):
        # Add an issuer key on Sovrin
        self._issuerPks[issuerPk.key] = issuerPk
        req = issuerPk.request
        if req:
            self.pendRequest(req, None)
        return len(self._pending)

    def getIssuerPublicKey(self, key=None, seqNo=None) -> Optional[
        IssuerPubKey]:
        assert key or seqNo
        if key:
            return self._issuerPks.get(key)
        else:
            for _, pk in self._issuerPks.items():
                if pk.seqNo == seqNo:
                    return pk
        return self._issuerPks.get(key)

    def getIssuerPublicKeyForClaimDef(self, issuerId, seqNo=None,
                                      claimDefKey=None, required=False) -> \
            Optional[IssuerPubKey]:
        notFoundMsg = "Issuer public key not found"
        if not seqNo:
            claimDef = self.getClaimDef(key=claimDefKey)
            if not claimDef:
                logger.info("Cannot get issuer key by claim def since claim "
                            "def not fetched yet: {}".format(claimDefKey))
                if required:
                    raise RuntimeError(notFoundMsg)
                return None
            else:
                seqNo = claimDef.seqNo
        ipk = self.getIssuerPublicKey(key=(issuerId, seqNo))
        if ipk:
            return ipk

        if required:
            raise RuntimeError(notFoundMsg)

    def getAllIssuerKeysForClaimDef(self, seqNo):
        return [ipk for ipk in self._issuerPks.values()
                if ipk.claimDefSeqNo == seqNo]

    def getAvailableClaimList(self):
        resp = []
        for k, v in self._claimDefs.items():
            ipks = self.getAllIssuerKeysForClaimDef(v.seqNo)
            resp.extend([(v, ipk) for ipk in ipks])
        return resp

    def isClaimDefComplete(self, claimDefKey):
        claimDef = self.getClaimDef(key=claimDefKey)
        return claimDef and claimDef.seqNo

    def isIssuerKeyComplete(self, origin, reference):
        ipk = self.getIssuerPublicKey(key=(origin, reference))
        return ipk and ipk.seqNo
