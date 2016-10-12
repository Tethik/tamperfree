import requests
import re
import os
from os.path import join
from subprocess import call
import sys
import logging

DIST_URL = "https://dist.torproject.org/torbrowser/"
logger = logging.getLogger(__name__)

def _current_tor_browser_version(dir):
    try:
        with open(join(dir, "browser_version")) as f:
            return f.read()
    except:
        return "0.0.0"

def download_latest_tor_browser_version(dir):
    try:
        os.makedirs(dir)
    except:
        pass
    print("Finding the latest version of Tor Browser.")
    dist = requests.get(DIST_URL)
    # Versions are numbers in the form of X.Y.Z
    versions = re.findall('\d\.\d\.\d', dist.text)
    latest_version = sorted(versions)[-1]
    installed_version = _current_tor_browser_version(dir)

    if installed_version >= latest_version:
        print("Latest version is already downloaded. Quitting.")
        return

    filename = "tor-browser-linux64-{version}_en-US.tar.xz".\
        format(version=latest_version)
    url = "https://dist.torproject.org/torbrowser/{version}/{filename}".\
        format(version=latest_version, filename=filename)

    print("Downloading Tor Browser version {version}.".\
        format(version=latest_version))
    r = requests.get(url, stream=True)
    localfile = join(dir, filename)
    print(localfile)
    with open(localfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    print("Extracting...")
    # Decompress using tar xf
    if call(["tar", "xf", filename], cwd=dir):
        logger.error("Decompression using `tar` failed. Is tar installed?")
        return

    os.remove(localfile)
    with open(join(dir, "browser_version"), "w") as f:
        f.write(latest_version)

    print("Latest version is now downloaded.")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    download_latest_tor_browser_version(".")
