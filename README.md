# tamperfree
A tool for verifying static content Tor Hidden Service websites using requests
that are indistinguishable from real visitor requests.

*Please note that this is a prototype only. As such I don't want to make any promises of any real security.
There may be bugs and/or security vulnerabilities*.

# install
You will need Xvfb in order to run this program. It's so that selenium  
can run the browser headless.

On fedora:
`dnf install xorg-x11-server-Xvfb`

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

## notes
1. Http Works. (Although injection by exit node could mess with results)
2. Https does not work because it's encrypted before it reaches proxy.
3. Tor-hidden service works.


## todo
1. Tests.
2. Packaging (fedora for now, since that's what I'm running).

## issues
Does not verify the order of requests. Meaning that the server could perhaps(?)
order the scripts in such a way to maliciously get a different behaviour.

Sometimes the Browser will not connect. Unsure why. Might be due to Tor issues.
Like a bad Exit node or something.

Lots of folders are created in /tmp/ by Selenium. At least for me on a smaller
vm this leads to disk space running out.

alert("lel") stops the verification...

The HTTP parsing will probably have to be improved. I think it can be tricked by
the server sending HTTP status messages inside a body. If this trick works, I
think the verifier will crash because there are more responses than requests.

# testing
My burn service: npjhj3yqy7e7xntn.onion
