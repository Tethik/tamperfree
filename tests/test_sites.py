from stem.control import Controller
import stem.process
from flask import request
import threading
import multiprocessing
import os
import pytest

from tamperfree.main import stamp, verify
from tamperfree.verify import MismatchedHashes, MissingHashes, ExtraneousHashes
from tamperfree.browser import ProxiedBrowser
from tamperfree.tor_process import TorProcess

from os.path import join, abspath

import sample_sites.basic
import sample_sites.extra
import sample_sites.missing
import sample_sites.tampered

import requests
from time import sleep
import logging, sys

class MicroMock(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

TOR_EXECUTABLE_DIR = "tor-browser_en-US/Browser/TorBrowser/Tor"
TORRC_PATH = "tor-browser_en-US/Browser/TorBrowser/Data/Tor/torrc-defaults"

@pytest.fixture(scope="session")
def hidden_service(datadir):
    path = abspath(join(datadir,TOR_EXECUTABLE_DIR))
    os.environ["LD_LIBRARY_PATH"] = path
    cmd = path + "/tor"
    tor_process = stem.process.launch_tor_with_config(
      tor_cmd = cmd,
      take_ownership = True,
      config = {
        'SocksPort': str(9999),
        'ControlPort': str(9998),
      },
    )
    controller = Controller.from_port(port=9998)
    controller.authenticate()
    result = controller.create_ephemeral_hidden_service({ 80: 5000 }, await_publication = True)
    onion = "http://" + result.service_id + ".onion"
    yield onion
    # cleanup
    controller.close()
    tor_process.kill()

@pytest.fixture()
def run_app():
    class zzz:
        p = None

    def function(app, port):
        @app.route('/kill')
        def kill():
            request.environ.get('werkzeug.server.shutdown')()
            return ""

        @app.route('/status')
        def status():
            return "1"

        def run_server():
            print("starting app..")
            app.run(host="127.0.0.1", port=port)

        zzz.p = multiprocessing.Process(target=run_server)
        zzz.p.start()

        #try until we can connect
        while True:
            url = 'http://127.0.0.1:{}/status'.format(port)
            print("Trying to connect to server.", url)
            try:
                requests.get(url)
                break
            except:
                pass


    yield function

    if zzz.p:
        zzz.p.terminate()


def test_basic_site(datadir, hidden_service, run_app):
    run_app(sample_sites.basic.app, 5000)
    logging.basicConfig(stream=sys.stderr, level="INFO")
    args = MicroMock(url=hidden_service, dir=datadir, tor_port=9999, launch_tor=False, log_level="INFO")
    stamp(args)
    result, reasons = verify(args)
    assert result
    assert reasons == []

def test_extra_site(datadir, hidden_service, run_app):
    run_app(sample_sites.extra.app, 5000)
    args = MicroMock(url=hidden_service, dir=datadir, tor_port=9999, launch_tor=False, log_level="INFO")
    stamp(args)
    result, reasons = verify(args)
    print(reasons)
    assert not result
    assert any(isinstance(r, MismatchedHashes) for r in reasons)
    assert any(isinstance(r, ExtraneousHashes) for r in reasons)

def test_missing_site(datadir, hidden_service, run_app):
    run_app(sample_sites.missing.app, 5000)
    args = MicroMock(url=hidden_service, dir=datadir, tor_port=9999, launch_tor=False, log_level="INFO")
    stamp(args)
    result, reasons = verify(args)
    print(reasons)
    assert not result
    assert any(isinstance(r, MismatchedHashes) for r in reasons)
    assert any(isinstance(r, MissingHashes) for r in reasons)

def test_tampered_site(datadir, hidden_service, run_app):
    run_app(sample_sites.tampered.app, 5000)
    args = MicroMock(url=hidden_service, dir=datadir, tor_port=9999, launch_tor=False, log_level="INFO")
    stamp(args)
    result, reasons = verify(args)
    print(reasons)
    assert not result
    assert any(isinstance(r, MismatchedHashes) for r in reasons)

def test_my_burn_service(datadir):
    args = MicroMock(url="http://npjhj3yqy7e7xntn.onion", dir=datadir, tor_port=9999, launch_tor=False, log_level="INFO")
    stamp(args)
    result, reasons = verify(args)
    assert result
    assert len(reasons) == 0

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level="INFO")
    datadir = "../.tamperfree_data"
    onion = next(hidden_service(datadir))
    f = next(run_app())
    f(sample_sites.basic.app)
    browser = ProxiedBrowser(datadir, proxy_port=1234, tor_port=9999)
    browser.open()
    print(onion)
    pytest.set_trace()
