"""Plone Distribution support."""

from pathlib import Path

import logging


DEFAULT_PATH = Path(__file__).parent / "default"
PACKAGE_NAME = "plone.distribution"
DEFAULT_PROFILE = "Products.CMFPlone:plone"


logger = logging.getLogger(PACKAGE_NAME)
