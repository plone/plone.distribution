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
        assert len(distributions) >= 2
        # First distribution will be default
        dist = distributions[0]
        assert dist.name == "default"

    @pytest.mark.parametrize("name", ["default", "classic"])
    def test_get_success(self, integration, name):
        dist = dist_api.get(name=name)
        assert isinstance(dist, Distribution)
        assert dist.name == name

    @pytest.mark.parametrize("name", ["not_there", "fake"])
    def test_get_fail(self, integration, name):
        with pytest.raises(ValueError) as exc:
            dist_api.get(name=name)
        assert f"No distribution named {name}" in str(exc)
