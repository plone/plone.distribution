from io import BytesIO
from plone.distribution.utils import request as utils_request
from zope.component import provideAdapter
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.publisher.browser import BrowserLanguages
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.HTTPRequest import HTTPRequest

import pytest


class TestUtilsRequest:
    @pytest.mark.parametrize(
        "language,expected",
        [
            ("en-US,en;q=0.5", "en-us"),
            ("pt-BR,pt;q=0.5", "pt-br"),
            ("pt-BO,pt;q=0.5", "pt"),
            ("pt-PT,pt;q=0.5", "pt"),
            ("en;q=0.5", "en"),
            ("es;q=0.5", "es"),
            ("de;q=0.5", "de"),
        ],
    )
    def test_extract_browser_language(self, language, expected):
        provideAdapter(BrowserLanguages, [IHTTPRequest], IUserPreferredLanguages)
        request = HTTPRequest(
            BytesIO(),
            {
                "HTTP_ACCEPT_LANGUAGE": language,
                "SERVER_NAME": "nohost",
                "SERVER_PORT": "8080",
            },
            None,
        )
        value = utils_request.extract_browser_language(request)
        assert value == expected
