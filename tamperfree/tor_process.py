from subprocess import Popen
from os.path import join, abspath

TOR_EXECUTABLE_DIR = "tor-browser_en-US/Browser/TorBrowser/Tor"
TORRC_PATH = "tor-browser_en-US/Browser/TorBrowser/Data/Tor/torrc"

def start_tor(dir):
    cmd = "LD_LIBRARY_PATH={path} {path}/tor -f {torrc}".\
        format(path=abspath(join(dir,TOR_EXECUTABLE_DIR)),
            torrc=abspath(join(dir, TORRC_PATH)))
    process = Popen(cmd, shell=True)
    return process

if __name__ == "__main__":
    start_tor("").communicate()
