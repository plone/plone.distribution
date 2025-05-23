from pathlib import Path
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution

import pytest


class TestApiDistribution:
    def test_get_registry(self, integration):
        from plone.distribution.registry import DistributionRegistry

        registry = dist_api.get_registry()
        assert isinstance(registry, DistributionRegistry)

    def test_get_distributions(self, integration):
        distributions = dist_api.get_distributions()
        # In this package we have already 2 distributions
        assert len(distributions) >= 1
        # First distribution will be default
        dist = distributions[0]
        assert dist.name == "testing"

    @pytest.mark.parametrize(
        "name, title, package",
        [("testing", "Testing Plone Site", "plone.distribution.testing")],
    )
    def test_get_success(self, integration, name: str, title: str, package: str):
        dist = dist_api.get(name=name)
        assert isinstance(dist, Distribution)
        assert repr(dist) == f"<Distribution name='{name}' title='{title}'>"
        assert dist.name == name
        assert dist.title == title
        assert dist.package == package
        assert isinstance(dist.schema, dict)
        assert isinstance(dist.uischema, dict)
        assert isinstance(dist.image, Path)

    @pytest.mark.parametrize("name", ["not_there", "fake"])
    def test_get_fail(self, integration, name):
        with pytest.raises(ValueError) as exc:
            dist_api.get(name=name)
        assert f"No distribution named {name}" in str(exc)
