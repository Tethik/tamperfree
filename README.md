# tamperfree
A tool for verifying static content Tor Hidden Service websites using requests
that are indistinguishable from real visitor requests.

*Please note that this is a prototype only. As such I don't want to make any promises of any real security.
There may be bugs and/or security vulnerabilities*.

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


## issues
Does not verify the order of requests. Meaning that the server could perhaps(?)
order the scripts in such a way to maliciously get a different behaviour.

Sometimes the Browser will not connect. Unsure why. Might be due to Tor issues.
Like a bad Exit node or something.

Lots of folders are created in /tmp/ by Selenium. At least for me on a smaller
vm this leads to disk space running out.

alert("lel") stops the verification...

# testing
My burn service: npjhj3yqy7e7xntn.onion
