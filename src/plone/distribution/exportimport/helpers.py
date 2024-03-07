from pathlib import Path
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution
from plone.distribution.exportimport.interfaces import ExportFormat
from plone.distribution.exportimport.interfaces import ExportStep
from typing import List

import json
import os
import shutil


EXPORT_STEPS_BASE = [
    ("discussion", True),
    ("ordering", True),
    ("redirects", True),
    ("relations", True),
    ("translations", True),
]

EXPORT_STEPS_CLASSIC_UI = [
    ("portlets", True),
    ("defaultpages", True),
]

EXPORT_STEPS_MEMBERS = [
    ("members", False),
    ("localroles", False),
]

ALL_EXPORT_STEPS = EXPORT_STEPS_BASE + EXPORT_STEPS_CLASSIC_UI + EXPORT_STEPS_MEMBERS


def filter_devel_distributions(name: str = "") -> List[Distribution]:
    """List of distributions still in development."""
    distributions = []
    devel_distributions = os.environ.get("DEVELOP_DISTRIBUTIONS", "")
    for dist_name in devel_distributions.split(","):
        if name and dist_name != name:
            continue
        try:
            distribution = dist_api.get(name=dist_name)
        except ValueError:
            # Distribution does not exist
            continue
        else:
            distributions.append(distribution)
    return distributions


def remove_site_root(item: dict, portal_url: str) -> dict:
    """Remove references to site root from exported content."""
    item_str = json.dumps(item)
    replacements = [
        (f'"@id": "{portal_url}/', '"@id": "/'),
        (f'"@id": "{portal_url}"', '"@id": "/"'),
        (f'"url": "{portal_url}/', '"url": "/'),
    ]
    for pattern, replace in replacements:
        item_str = item_str.replace(pattern, replace)
    return json.loads(item_str)


def exports_for_distribution(distribution: Distribution) -> List[ExportStep]:
    """Return a list of available exports for a given distribution."""
    _exports = []
    _exports.extend(EXPORT_STEPS_BASE)
    directory = distribution.directory
    if not distribution.headless:
        _exports.extend(EXPORT_STEPS_CLASSIC_UI)
    for name, selected in EXPORT_STEPS_MEMBERS:
        already_exported = (directory / f"{name}.json").exists()
        selected = True if already_exported else selected
        _exports.append((name, selected))
    return [ExportStep(name, selected) for name, selected in _exports]


def remove_path(path: Path):
    """Remove existing files from a path"""
    shutil.rmtree(path, ignore_errors=True)


def sniff_export_format(path: Path) -> ExportFormat:
    """Identify what export format was used."""
    items_subdir = path / "items"
    if items_subdir.exists() and items_subdir.is_dir():
        return ExportFormat.SPLIT
    return ExportFormat.ONE_FILE
