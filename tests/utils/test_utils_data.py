from plone.distribution.utils import data as utils_data

import pytest


class TestUtilsStaConvertDataURI:
    @property
    def func(self):
        return utils_data.convert_data_uri_to_b64

    @pytest.mark.parametrize(
        "value,expected",
        [
            [
                "name=teste;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",  # noQA
                b"filenameb64:dGVzdGU7ZGF0YTppbWFnZS9wbmc=;datab64:iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",  # noQA
            ],
            ["", b""],
        ],
    )
    def test_check_conversion(self, value: str, expected: bytes):
        result = self.func(value)
        assert result == expected
