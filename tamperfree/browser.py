from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import hashlib
from tamperfree.proxy import TCP
import logging
import sys
from time import sleep
from tamperfree.http import extract_from_capturefile
from tamperfree.tor_process import start_tor
from os.path import join
import os
from xvfbwrapper import Xvfb

logger = logging.getLogger(__name__)

FIREFOX_PATH = "tor-browser_en-US/Browser/start-tor-browser"
FIREFOX_PROFILE = "tor-browser_en-US/Browser/TorBrowser/Data/Browser/profile.default/"

class ProxiedBrowser(object):
    def __init__(self, dir, proxy_port):
        self.dir = dir
        self.proxy_port = int(proxy_port)


    def __enter__(self):
        cap_dir = join(self.dir, "caps")
        try:
            os.makedirs(cap_dir)
        except:
            pass
        self.proxy = TCP(cap_dir=cap_dir, port=self.proxy_port)
        self.proxy.start()
        logger.info("Starting Tor process..")
        self.tor = start_tor(self.dir)
        while not self.proxy.running:
            logger.info("Waiting for proxy to start...")
            sleep(1)

        logger.info("Starting Xvfb virtual display")
        self.vdisplay = Xvfb(width=1280, height=740)
        self.vdisplay.start()

        logger.info("Webdriver starting..")

        self.binary = FirefoxBinary(firefox_path=join(self.dir, FIREFOX_PATH), log_file=open("firefox.log", "w"))
        self.binary.add_command_line_options("--verbose")
        self.profile = FirefoxProfile(profile_directory=join(self.dir, FIREFOX_PROFILE))
        self.profile.set_preference("network.proxy.socks_port", self.proxy_port)
        self.profile.set_preference("extensions.torlauncher.start_tor", False)
        self.profile.update_preferences()

        try:
            self.driver = webdriver.Firefox(firefox_binary=self.binary, firefox_profile=self.profile)
            sleep(10) # wait until homepage etc have loaded.
        except Exception as ex:
            self.proxy.close()
            raise ex

        return self

    def get(self, url):
        logger.info("Fetching {url}".format(url=url))
        self.proxy.consume_results() # clear anything previous, e.g the browsers homepage
        self.driver.get(url)
        sleep(30) # lazy way of ensuring that the whole page gets loaded.
        capture_files = self.proxy.consume_results()
        responses = list()
        for capture_file in capture_files:
            responses += extract_from_capturefile(capture_file)
            os.remove(capture_file)
        return responses

    def __exit__(self, type, value, traceback):
        logging.info("Closing Webdriver")
        self.driver.close()
        logging.info("Closing virtual display")
        self.vdisplay.stop()
        logging.info("Closing Proxy")
        self.proxy.close()
        logger.info("Closing Tor")
        self.tor.kill()

class ProxiedBrowserResponse(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    with ProxiedBrowser("", 8899) as b:
        r = b.get("http://ip.blacknode.se/")
        logging.info("Hashes:")
        for _r in r:
            h = hashlib.sha256()
            if isinstance(_r, bytes):
                h.update(_r)
            else:
                h.update(_r.encode('utf-8'))
            logger.info(h.hexdigest())
