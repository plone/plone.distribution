"""Plone Distribution support."""

from pathlib import Path

import logging


BASE_DISTRIBUTIONS_PATH = Path(__file__).parent / "distributions"
PACKAGE_NAME = "plone.distribution"

logger = logging.getLogger(PACKAGE_NAME)
