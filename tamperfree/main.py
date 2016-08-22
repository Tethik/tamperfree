import sys
import argparse
from tamperfree.version import *

def main(args):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('url', help='Url to hidden service or website to verify.')
    parser.add_argument('git', help='Git repository to verify against')
    parser.add_argument('--proxy-port', default='8899', help='Port used to eavesdrop on traffic between the Tor browser and the Tor proxy')
    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO, WARNING, ERROR, CRITICAL')
    args = parser.parse_args()

    main(args)
