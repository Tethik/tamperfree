import sys
import argparse
from tamperfree.version import *


def verify(url):
    pass

def stamp(url):
    pass

def gitstamp():
    """
    Todo: idea to point to a git repository, clone and build proper verification set.
    """
    pass

def main(args):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('url', help='Url to hidden service or website to verify.')
    # parser.add_argument('git', help='Git repository to verify against')
    parser.add_argument('--proxy-port', default='8899', help='Port used to eavesdrop on traffic between the Tor browser and the Tor proxy')
    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--stamp', default=False, help="""
    Stamp the current version fetched from {url} as version. This will
    create a set of secure hashes based on the responses returned when accessing
    the url in the Tor Browser.""")
    parser.add_argument('--verify', default=True, help="""
    Perform a verification on the given {url} based on a saved stamp. This requires that
    a stamp has been performed beforehand so that the verifier has something to compare against.
    """)
    parser.add_argument('--single', default=True, help='Whether or not only the given url will be crawled.')
    parser.add_argument('--crawl', default=False, help='Whether or not the url should be crawled on all links')
    args = parser.parse_args()

    main(args)
