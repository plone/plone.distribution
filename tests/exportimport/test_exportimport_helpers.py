from pathlib import Path
from plone.distribution.exportimport import helpers

import json
import pytest


class TestFilterDistributions:
    env_var: str = "DEVELOP_DISTRIBUTIONS"

    @pytest.mark.parametrize(
        "var_value,expected",
        [
            ("", []),
            ("classic", ["classic"]),
            ("default", ["default"]),
            ("classic,default", ["classic", "default"]),
            ("default,classic", ["classic", "default"]),
            ("foo", []),
        ],
    )
    def test_filter_devel_distributions(
        self, integration, monkeypatch, var_value, expected
    ):
        monkeypatch.setenv(self.env_var, var_value)
        distributions = helpers.filter_devel_distributions()
        assert isinstance(distributions, list)
        assert len(distributions) == len(expected)
        for distribution in distributions:
            assert distribution.name in expected


@pytest.fixture
def export_item() -> dict:
    """Plone Site serialization."""
    export_item_path = Path(__file__).parent / "portal.json"
    return json.loads(export_item_path.read_text())[0]


class TestItemHelpers:
    SITE_ROOT: str = "http://localhost:8080/Plone"
    IMG_BLOCK_UID: str = "29a6a70d-321a-4747-99a0-a18267c79a87"
    GRID_BLOCK_UID: str = "b2da3173-7984-45ae-b00e-61801faf80a6"

    def _get_img_block(self, item: dict) -> dict:
        block = item["blocks"][self.IMG_BLOCK_UID]
        return block

    def _get_grid_block_column(self, block: dict) -> dict:
        # Return the first column
        column = block["columns"][0]
        return column

    def _get_grid_block(self, item: dict) -> dict:
        return item["blocks"][self.GRID_BLOCK_UID]

    def test_remove_site_root_from_id(self, integration, export_item):
        func = helpers.remove_site_root
        result = func(export_item, self.SITE_ROOT)
        assert export_item["@id"].startswith(self.SITE_ROOT)
        assert result["@id"] == "/"

    def test_remove_site_root_from_image_block(self, integration, export_item):
        func = helpers.remove_site_root
        src_block = self._get_img_block(export_item)
        assert src_block["url"].startswith(self.SITE_ROOT)

        result = func(export_item, self.SITE_ROOT)
        result_block = self._get_img_block(result)
        assert result_block["url"].startswith("/")
