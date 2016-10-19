*Please note that this is a prototype only. As such I don't want to make any promises of any real security. There may be bugs and/or security vulnerabilities*.

# tamperfree
A tool for verifying static content Tor Hidden Service websites using requests
that are indistinguishable from real visitor requests. The idea is that by running
this tool often enough you can detect if the site is being tampered with. This could
for example be useful as having at least some guarantee that a javascript crypto
client has integrity.

# install
You will need Xvfb in order to run this program. It's so that selenium, the framework used to control Tor Browser, can run the browser without a visible window (headless).

On fedora:
`dnf install xorg-x11-server-Xvfb`

`git clone https://github.com/Tethik/tamperfree`

`python setup.py install`

I plan to eventually package this nicely.

## usage
To update/download the latest tor browser version for selenium to use.
`tamperfree update_browser`

First "stamp" the site. This will save a secure hash of every path visited on
the website.
`tamperfree stamp <onionurl>`

To then verify it, run the following command. It will fetch a new set of hashes
and compare them to the ones that were stamped earlier. It will tell you which
path has been tampered with, which paths were missing or which were added.
`tamperfree verify <onionurl>`

# testing
You can run the tests via.
`py.test`
My burn service: npjhj3yqy7e7xntn.onion
