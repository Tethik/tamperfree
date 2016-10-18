from tamperfree.main import check_and_fix_url, UnsupportedUrl, NotAHiddenService, UnsupportedUrl
from pytest import raises

def test_check_and_fix_url_ok():
    assert check_and_fix_url("http://anything.onion") == "http://anything.onion"

def test_check_and_fix_url_fix():
    assert check_and_fix_url("anything.onion") == "http://anything.onion"

def test_check_and_fix_url_https_should_fail():
    with raises(UnsupportedUrl):
        check_and_fix_url("https://anything.xxx")

def test_check_and_fix_url_not_onion_should_fail():
    with raises(NotAHiddenService):
        check_and_fix_url("http://anything.xxx")

def test_check_and_fix_url_not_onion_should_fail():
    with raises(UnsupportedUrl):
        check_and_fix_url("ftp://anything.onion")
