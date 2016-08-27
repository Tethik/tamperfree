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

logger = logging.getLogger(__name__)

class ProxiedBrowser(object):
    def __init__(self, proxy_port):
        self.proxy_port = int(proxy_port)
        self.binary = FirefoxBinary(firefox_path="./tor-browser_en-US/Browser/start-tor-browser", log_file=open("firefox.log", "w"))
        self.profile = FirefoxProfile(profile_directory="./tor-browser_en-US/Browser/TorBrowser/Data/Browser/profile.default/")
        self.profile.set_preference("network.proxy.socks_port", self.proxy_port)
        self.profile.update_preferences()


    def __enter__(self):
        self.proxy = TCP(port=self.proxy_port)
        self.proxy.start()
        while not self.proxy.running:
            logger.info("Waiting for proxy to start...")
            sleep(1)

        logger.info("Webdriver starting..")
        self.driver = webdriver.Firefox(firefox_binary=self.binary, firefox_profile=self.profile)


        # Set up the proxy settings.
        # proxy_host = 'localhost'
        # self.profile.set_preference("network.proxy.type", 1)
        # self.profile.set_preference("network.proxy.http", proxy_host)
        # self.profile.set_preference("network.proxy.http_port", self.proxy_port)
        # self.profile.set_preference("network.proxy.https", proxy_host)
        # self.profile.set_preference("network.proxy.https_port", self.proxy_port)
        # self.profile.set_preference("network.proxy.ssl", proxy_host)
        # self.profile.set_preference("network.proxy.ssl_port", self.proxy_port)
        # self.profile.set_preference("network.proxy.ftp", proxy_host)
        # self.profile.set_preference("network.proxy.ftp_port", self.proxy_port)
        # self.profile.set_preference("network.proxy.socks", proxy_host)


        # self.profile.set_preference("extensions.torbutton.banned_ports", "{socks_port},{control_port}".format(self.proxy_port, self.tor_control_port))
        # self.profile.set_preference("extensions.torbutton.block_disk", False)
        # self.profile.set_preference("extensions.torbutton.custom.socks_host", proxy_host)
        # self.profile.set_preference("extensions.torbutton.custom.socks_port", self.proxy_port)
        # self.profile.set_preference("extensions.torbutton.inserted_button", True)
        # self.profile.set_preference("extensions.torbutton.launch_warning", False)
        # self.profile.set_preference("extensions.torbutton.loglevel", 2)
        # self.profile.set_preference("extensions.torbutton.logmethod", 0)
        # self.profile.set_preference("extensions.torbutton.settings_method", "custom")
        # self.profile.set_preference("extensions.torbutton.socks_port", proxy_port)
        # self.profile.set_preference("extensions.torbutton.use_privoxy", False)
        # self.profile.set_preference("extensions.torlauncher.control_port", self.tor_control_port)
        # self.profile.set_preference("extensions.torlauncher.loglevel", 2)
        # self.profile.set_preference("extensions.torlauncher.logmethod", 0)
        # self.profile.set_preference("extensions.torlauncher.prompt_at_startup", False)
        # self.profile.set_preference("extensions.torlauncher.start_tor", False)
        return self

    def get(self, url):
        logger.info("Fetching {url}".format(url=url))
        self.proxy.consume_results() # clear anything previous, e.g the browsers homepage
        self.driver.get(url)
        sleep(5)
        capture_files = self.proxy.consume_results()
        responses = list()
        for capture_file in capture_files:
            for response in extract_from_capturefile(capture_file):
                logger.info(response.status_line)
                logger.info(response.headers)
                logger.info(response.body)
                responses.append(response.body)
        return responses

    def __exit__(self, type, value, traceback):
        logging.info("Closing Webdriver")
        self.driver.close()
        logging.info("Closing Proxy")
        self.proxy.close()

class ProxiedBrowserResponse(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    with ProxiedBrowser(8899) as b:
        r = b.get("http://ip.blacknode.se/")
        logging.info("Hashes:")
        for _r in r:
            h = hashlib.sha256()
            # logger.info(_r)
            if isinstance(_r, bytes):
                h.update(_r)
            else:
                h.update(_r.encode('utf-8'))
            logger.info(h.hexdigest())
