import sys
import argparse
from tamperfree.version import *
from tamperfree.browser_fetcher import download_latest_tor_browser_version
from tamperfree.verify import fetch_hashes
import logging

def update_browser(args):
    download_latest_tor_browser_version(args.dir)

def verify(args):
    print(args)
    s = fetch_hashes(args.url)
    print(s)

def stamp(args):
    print(args)
    s = fetch_hashes(args.url)

def main(args):
    args.func(args)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='sub-command help')
    parser_verify = subparsers.add_parser('verify', help="""
Perform a verification on the given {url} based on a saved stamp. This requires that
a stamp has been performed beforehand so that the verifier has something to compare against.
""")
    parser_verify.add_argument('url', help='Url to hidden service or website to verify.')
    parser_verify.set_defaults(func=verify)

    parser_stamp = subparsers.add_parser('stamp', help="""
Stamp the current version fetched from {url} as version. This will
create a set of secure hashes based on the responses returned when accessing
the url in the Tor Browser.""")
    parser_stamp.add_argument('url', help='Url to hidden service or website to verify.')
    parser_stamp.set_defaults(func=stamp)

    parser_update_browser = subparsers.add_parser('update_browser', help="""
Downloads the latest version of Tor Browser.
    """)
    parser_update_browser.set_defaults(func=update_browser)

    parser.add_argument('--proxy-port', default='8899', help='Port used to eavesdrop on traffic between the Tor Browser and the Tor proxy')
    parser.add_argument('--log-level', default='INFO', help='DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--dir', default='tamperfree_data', help='Directory used to store stamps and the Tor Browser executable.')
    #parser.add_argument('git', help='Git repository to verify against')
    #parser.add_argument('--single', default=True, help='Whether or not only the given url will be crawled.')
    #parser.add_argument('--crawl', default=False, help='Whether or not the url should be crawled on all links')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=args.log_level)
    main(args)
