from pathlib import Path
from plone.distribution.core import Distribution
from plone.distribution.registry import _distribution_registry
from plone.distribution.registry import DistributionRegistry
from typing import List

import os


base_folder = Path(__file__).parent.parent / "distributions"


def _allow_list() -> List[str]:
    """Return a list of allowed distributions."""
    allowed_distributions = os.environ.get("ALLOWED_DISTRIBUTIONS", "")
    if allowed_distributions:
        allowed_distributions = allowed_distributions.split(",")
    return allowed_distributions


def get_registry() -> DistributionRegistry:
    """Return the Distribution Registry."""
    return _distribution_registry


def get_distributions(filter: bool = True) -> List[Distribution]:
    """Get available Plone distributions."""
    registry = get_registry()
    all_distributions = registry.enumerate_distributions()
    allowed_distributions = _allow_list()
    if filter and allowed_distributions:
        return [d for d in all_distributions if d.name in allowed_distributions]
    return all_distributions


def get(name: str) -> Distribution:
    """Get a distribution."""
    registry = get_registry()
    distribution = registry.lookup(name)
    if not distribution:
        raise ValueError(f"No distribution named {name}")
    return distribution
