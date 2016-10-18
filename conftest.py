import pytest
import os
from tamperfree.browser_fetcher import download_latest_tor_browser_version

def pytest_addoption(parser):
    parser.addoption("--inconsiderate", action="store_true",
        help="run inconsiderate tests. These are tests that may rely on external services that I don't want to spam too much.")
    parser.addoption("--runslow", action="store_true",
        help="run slow tests.")


@pytest.fixture(scope="session")
def datadir():
    # Look for the local directory. If it doesnt exist, we probably need to download the tor browser.
    path = "tests/.tamperfree_data"
    if not os.path.exists(path):
        download_latest_tor_browser_version(path)

    return path
