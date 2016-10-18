import hashlib
import json
import logging
from tamperfree.browser import ProxiedBrowser
from tamperfree.tor_process import TorProcess

logger = logging.getLogger(__name__)

class MismatchedHashes(object):
    def __init__(self, hashes, wrong_hashes):
        self.hashes = hashes
        self.wrong_hashes = wrong_hashes

    def __str__(self):
        return "The following hashes do not match with the stamped hashes:\n{}".\
            format("\n".join([k + " " + v + "(expected: " + self.hashes[k] + ")" for k,v in self.wrong_hashes]))

class MissingHashes(object):
    def __init__(self, missing_hashes):
        self.hashes = missing_hashes

    def __str__(self):
        return "Missing hashes:\n{}".\
            format("\n".join([str(v) for v in self.hashes]))

class ExtraneousHashes(object):
    def __init__(self, new_hashes):
        self.hashes = new_hashes

    def __str__(self):
        return "Extraneous hashes:\n{}".\
            format("\n".join([str(v) for v in self.hashes]))

class SiteContentStamp(object):
    def __init__(self, hashes = None):
        self.hashes = dict()
        if hashes:
            for k,v in hashes:
                self.hashes[k] = v

    def verify_against(self, other):
        """
        Look for differences between the hashes in this stamp and the other stamp.
        Looks for missing or new hashes, in case content has been deleted or added.
        Then it looks for hashes that do not match. The goal here is to try and
        explain the results as best as possible so that we know why something has
        gone wrong.

        Returns true and an empty list if the verification succeeded. Otherwise
        returns false and a list of reasons why the verification failed.
        """
        # O(n2)

        new_hashes = []
        wrong_hashes = []
        for k, v in other.hashes.iteritems():
            if k not in self.hashes:
                new_hashes.append((k, v))
            elif self.hashes[k] != v:
                wrong_hashes.append((k, v))

        missing_hashes = [k for k in self.hashes if k not in other.hashes]

        reasons = []
        if new_hashes:
            reasons.append(ExtraneousHashes(new_hashes))
        if missing_hashes:
            reasons.append(MissingHashes(missing_hashes))
        if wrong_hashes:
            reasons.append(MismatchedHashes(self.hashes, wrong_hashes))

        return len(reasons) == 0, reasons

    def add(self, _b):
        h = hashlib.sha256()
        h.update(_b.body)
        hash = h.hexdigest()
        self.hashes[_b.request.path] = hash
        logger.info("Added hash " + str((_b.request.path, hash)))
        return hash

    def __str__(self):
        return "\n".join([str(h) for h in self.hashes.iteritems()])

    def save(self, file):
        json.dump({ "hashes": list(self.hashes.iteritems()) }, open(file, "w"))


def _object_hook(dct):
    return SiteContentStamp(hashes=dct['hashes'])

def load(file):
    return json.load(open(file), object_hook=_object_hook)

def fetch_hashes(dir, url, tor_port = 9150, launch_tor = True):
    # Fetches the hashes for a single url.
    stamp = SiteContentStamp()
    def fetch_stamps():
        with ProxiedBrowser(dir, tor_port=tor_port) as b:
            r = b.get(url)
            for _r in r:
                stamp.add(_r)


    if launch_tor:
        with TorProcess(dir, port=tor_port):
            fetch_stamps()
    else:
        fetch_stamps()

    return stamp
