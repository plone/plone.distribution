from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""

setup(
    name="plone.distribution",
    version="1.0.0a6",
    description="Plone distribution support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
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
    packages=find_packages("src"),
    namespace_packages=["plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Plone",
        "setuptools",
        "z3c.unconfigure",
        "collective.exportimport>=1.9",
    ],
    extras_require={
        "test": [
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "plone.volto",
            "plone.app.testing",
            "plone.restapi[test]",
            "pytest",
            "pytest-cov",
            "pytest-plone>=0.2.0",
        ]
    },
    entry_points={
        "z3c.autoinclude.plugin": ["target = plone"],
    },
)
