from subprocess import Popen
from os.path import join, abspath
import logging
from time import sleep
import stem.process
import os

logger = logging.getLogger(__name__)

TOR_EXECUTABLE_DIR = "tor-browser_en-US/Browser/TorBrowser/Tor"
TORRC_PATH = "tor-browser_en-US/Browser/TorBrowser/Data/Tor/torrc-defaults"

class TorProcess(object):
    def __init__(self, dir, port=9150, control_port=9151):
        self.dir = dir
        self.port = port
        self.control_port = control_port

    def open(self):
        logger.info("Starting Tor process.")
        path = abspath(join(self.dir,TOR_EXECUTABLE_DIR))
        os.environ["LD_LIBRARY_PATH"] = path
        cmd = path + "/tor"
        self.process = stem.process.launch_tor_with_config(
          tor_cmd = cmd,
          take_ownership = True,
          config = {
            'SocksPort': str(self.port),
            'ControlPort': str(self.control_port),
          },
        )

    def __enter__(self):
        return self.open()

    def close(self):
        self.process.terminate()
        self.process.wait()
        logger.info("Closing Tor process.")

    def __exit__(self, type, value, traceback):
        return self.close()

if __name__ == "__main__":
    print("Starting tor...")
    start_tor(".tamperfree_data").communicate()
