import hashlib
import json
import logging
from tamperfree.browser import ProxiedBrowser

class SiteContentStamp(object):
    def __init__(self, hashes = None):
        self.hashes = set()
        if hashes:
            self.hashes = set(hashes)

    def verify_against(self, other):
        hashes = other.hashes
        reasons = []
        if len(self.hashes) > len(hashes):
            reasons.append("Missing content, supplied set has less hashes.")
        elif len(self.hashes) < len(hashes):
            reasons.append("Extraneous content, supplied set has more hashes. ")

        wrong_hashes = [h for h in hashes if h not in self.hashes]

        if len(wrong_hashes) > 0:
            reasons.append(
            "The following hashes do not match with the stamped hashes:\n{}".\
            format("\n".join(wrong_hashes)))

        return len(reasons) == 0, reasons

    def add(self, _b):
        h = hashlib.sha256()
        h.update(_b)
        self.hashes.add(h.hexdigest())

    def __str__(self):
        return "\n".join(self.hashes)

    def save(self, file):
        json.dump({ "hashes": list(self.hashes) }, open(file, "w"))


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
