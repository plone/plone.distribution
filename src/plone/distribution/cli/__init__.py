from plone import api
from plone.distribution.api.distribution import get_current_distribution
from plone.exportimport.exporters import get_exporter
from plone.exportimport.utils import cli as cli_helpers

import argparse
import sys


CLI_SPEC = {
    "exporter": {
        "description": "Export Plone Site content",
        "options": {
            "zopeconf": "Path to zope.conf",
            "site": "Plone site ID to export the content from",
            "--include-revisions": "Include revision history",
        },
    },
}


def _parse_args(description: str, options: dict, args: list):
    parser = argparse.ArgumentParser(description=description)
    for key, help in options.items():
        if key.startswith("-"):
            parser.add_argument(key, action="store_true", help=help)
        else:
            parser.add_argument(key, help=help)
    namespace, _ = parser.parse_known_args(args[1:])
    return namespace


def export(args=sys.argv):
    """Export a Plone site to a distribution."""
    logger = cli_helpers.get_logger("Exporter")
    exporter_cli = CLI_SPEC["exporter"]
    # We get an argparse.Namespace instance.
    namespace = _parse_args(exporter_cli["description"], exporter_cli["options"], args)
    app = cli_helpers.get_app(namespace.zopeconf)
    site = cli_helpers.get_site(app, namespace.site, logger)
    distribution = get_current_distribution(site)
    path = distribution.directory / "content"
    if not path:
        logger.error(f"{namespace.path} does not exist, please create it first.")
        sys.exit(1)
    logger.info(f"Exporting Plone site at /{site.id}")
    logger.info(f" Target path: {path}")
    with api.env.adopt_roles(["Manager"]):
        results = get_exporter(site).export_site(path, options=namespace)
    for item in results[1:]:
        logger.info(f" Wrote {item.relative_to(path)}")
