from pathlib import Path
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""

setup(
    name="plone.distribution",
    version="4.0.0a2",
    description="Plone distribution support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    keywords="Plone CMF Python Zope CMS Distribution",
    author="Plone Foundation",
    author_email="releasemanager@plone.org",
    url="https://plone.org",
    license="GPL version 2",
    project_urls={
        "Homepage": "https://plone.org",
        "Documentation": "https://6.docs.plone.org",
        "Source": "https://github.com/plone/plone.distribution",
        "Issues": "https://github.com/plone/plone.distribution/issues",
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Products.CMFPlone",
        "Products.GenericSetup",
        "Zope",
        "jsonschema",
        "plone.api",
        "plone.base",
        "plone.dexterity",
        "plone.exportimport>=1.0.0b1",
        "plone.i18n",
        "plone.protect",
        "plone.rest",
        "plone.restapi",
        "z3c.unconfigure",
    ],
    extras_require={
        "test": [
            "plone.app.iterate",
            "plone.app.testing",
            "plone.app.upgrade",
            "plone.restapi[test]",
            "plone.volto[test]",
            "plone.testing",
            "pytest-cov",
            "pytest-plone>=0.5.0",
            "pytest",
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
        ]
    },
    entry_points={
        "z3c.autoinclude.plugin": ["target = plone"],
        "console_scripts": [
            "export-distribution = plone.distribution.cli:export",
        ],
    },
)
