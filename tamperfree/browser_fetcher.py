import requests
import re
import os
from os.path import join
from subprocess import call
import sys
import logging

DIST_URL = "https://dist.torproject.org/torbrowser/"
logger = logging.getLogger(__name__)

def download_latest_tor_browser_version(dir):
    try:
        os.makedirs(dir)
    except:
        pass
    logger.info("Finding the latest version of Tor Browser.")
    dist = requests.get(DIST_URL)
    # Versions are numbers in the form of X.Y.Z
    versions = re.findall('\d\.\d\.\d', dist.text)
    latest_version = sorted(versions)[-1]
    filename = "tor-browser-linux64-{version}_en-US.tar.xz".\
        format(version=latest_version)
    url = "https://dist.torproject.org/torbrowser/{version}/{filename}".\
        format(version=latest_version, filename=filename)

    logger.info("Downloading Tor Browser version {version}.".\
        format(version=latest_version))
    r = requests.get(url, stream=True)
    localfile = join(dir, filename)
    with open(localfile, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    logger.info("Extracting...")
    # Decompress using tar xf
    if call(["tar", "xf", localfile]):
        logger.error("Decompression using `tar` failed. Is tar installed?")
        return

    os.remove(localfile)
    logger.info("Latest version is downloaded.")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    download_latest_tor_browser_version(".")
