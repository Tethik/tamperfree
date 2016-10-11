import hashlib
import json
import logging
from tamperfree.browser import ProxiedBrowser

class SiteContentStamp(object):
    def __init__(self, hashes = None):
        self.hashes = dict()
        if hashes:
            for k,v in hashes:
                self.hashes[k] = v

    def verify_against(self, other):
        # O(n2)
        reasons = []
        if len(self.hashes) > len(other.hashes):
            reasons.append("Missing content, supplied set has less hashes.")
        elif len(self.hashes) < len(other.hashes):
            reasons.append("Extraneous content, supplied set has more hashes. ")

        wrong_hashes = [(k,v,self.hashes[k]) for k,v in other.hashes.iteritems() if self.hashes[k] != v]

        if len(wrong_hashes) > 0:
            reasons.append(
            "The following hashes do not match with the stamped hashes:\n{}".\
            format("\n".join([str(h) for h in wrong_hashes])))

        return len(reasons) == 0, reasons

    def add(self, _b):
        h = hashlib.sha256()
        h.update(_b.body)
        hash = h.hexdigest()
        self.hashes[_b.request.path] = hash
        print(_b.request.path, hash)
        return hash

    def __str__(self):
        return "\n".join([str(h) for h in self.hashes.iteritems()])

    def save(self, file):
        json.dump({ "hashes": list(self.hashes.iteritems()) }, open(file, "w"))


def _object_hook(dct):
    return SiteContentStamp(hashes=dct['hashes'])

def load(file):
    return json.load(open(file), object_hook=_object_hook)

def fetch_hashes(dir, url):
    # Fetches the hashes for a single url.
    stamp = SiteContentStamp()
    with ProxiedBrowser(dir, 8899) as b:
        r = b.get(url)
        for _r in r:
            stamp.add(_r)
    return stamp
