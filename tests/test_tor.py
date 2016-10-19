from flags import inconsiderate
from tamperfree.browser import ProxiedBrowser
from tamperfree.browser_fetcher import download_latest_tor_browser_version
from tamperfree.tor_process import TorProcess

@inconsiderate
def test_download_tor_browser(datadir):
    download_latest_tor_browser_version(datadir)

@inconsiderate
def test_is_tor_being_used(datadir):
    url = "https://check.torproject.org"
    with TorProcess(datadir):
        with ProxiedBrowser(datadir, 8899) as browser:
            browser.driver.get(url)
            print(browser.driver.title)
            assert "Congratulations. This browser is configured to use Tor." in browser.driver.title
