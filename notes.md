# Notes
This is just some of my own ramblings / notes as I develop this tool.

## todo
1. Packaging (fedora for now, since that's what I'm sort of running).
2. Refactor http parsing.
3. Uniform random for running the program over a period of time. How do we do this?
4. Crawling? Although I feel that ruins the indistinguishable part in terms of
user behaviour.

## issues / notes
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

Probably lots of ways to get the process to hang / error.

Is mostly inconsiderate to my Ctrl+C interrupts. Rude.

Those sleep statements are pretty lame. Should be possible to run this faster.

Not sure how this will perform for very large websites.

Favicon.ico issues. Sometimes loads more than once? Sometimes is missing?

Speaking of loading, I think current code only saves one hash, even if the same
path is loaded twice. If script.js has evil code that triggers after X loads
this will not detect that. What does the browser do if a js is loaded twice? is it cached?
