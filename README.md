# tamperfree
A tool for verifying static content Tor Hidden Service websites.

*Please note that this is a prototype only. As such I don't want to make any promises of any real security.
There may be bugs and/or security vulnerabilities*.

## notes
1. Http Works. (Although injection by exit node could mess with results)
2. Https does not work because it's encrypted before it reaches proxy.
3. Tor-hidden service works.


## todo
1. Auto update tor browser.
2. Build verification set(?)
3. Fix Tor setup? (wont work without manual selection of bridge/non-bridge.)
  * found workaround for this. set torlauncher to start_tor = false in prefs.js, then proxy via normal tor.
4. Better http parsing. Separate requests from responses.

## issues
Does not verify the order of requests. Meaning that the server could perhaps order the scripts in such a way to maliciously get a different behaviour.

/tor-browser_en-US/Browser/TorBrowser/Data/Tor/torrc
/tor-browser_en-US/Browser/TorBrowser/Tor

$LD_LIBRARY_PATH=. ./tor
