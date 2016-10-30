*Please note that this is a prototype only. As such I don't want to make any promises of any real security. There may be bugs and/or security vulnerabilities*.

# tamperfree
A tool for verifying static content Tor Hidden Service websites using requests
that are indistinguishable from real visitor requests. The idea is that by running
this tool often enough you can detect if the site is being tampered with. This could
for example be useful as having at least some guarantee that a javascript crypto
client has integrity.

# install
You will need Xvfb in order to run this program. It's so that selenium, the 
framework used to control Tor Browser, can run the browser without a visible 
window (headless).

On fedora:

`dnf install xorg-x11-server-Xvfb`

Then clone the repository.

`git clone https://github.com/Tethik/tamperfree`

Install as a python package.

`python setup.py install`

I plan to eventually package this nicely as an rpm.

## usage
To update/download the latest tor browser version for selenium to use. By default it
will be stored in a ".tamperfree_data" directory along with any future stamps. 

`tamperfree update_browser`

First "stamp" the site. This will save a secure hash of every path visited on
the website.

`tamperfree stamp <onionurl>`

To then verify it, run the following command. It will fetch a new set of hashes
and compare them to the ones that were stamped earlier. It will tell you which
path has been tampered with, which paths were missing or which were added.

`tamperfree verify <onionurl>`

# testing
Make sure you have the test requirements installed.

`pip -r test-requirements.txt`

You can then run the tests via.

`py.test`

I manually test using my own burn service: http://npjhj3yqy7e7xntn.onion
