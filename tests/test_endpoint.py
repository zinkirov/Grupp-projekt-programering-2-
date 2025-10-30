import pytest
import flask
import ssl
from urllib import request, response
from application import app


def test_index_page_contains_body_tag():
    with request.urlopen("http://127.0.0.1:5000", timeout=10) as response:
        html = str(response.read())
        assert ">Start</a>" in html

        