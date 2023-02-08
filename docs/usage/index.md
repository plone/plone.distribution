# Using this package

```{toctree}
:maxdepth: 1
:hidden: true

package-structure
code-examples
```

First of all, a Plone Distribution is a Python Package that can be installed by `pip` and follows certain conventions.

## Create a new Plone Distribution

The Plone Community provides a `Cookiecutter` template to generate new Plone Distribution packages: [cookiecutter-plone-distribution](https://github.com/collective/cookiecutter-plone-distribution).

This template is active development and it will probably change its structure until a stable release of `plone.distribution` is made.

### Basic Setup

To use the template, first, install `Cookiecutter` via command line:

```shell
pip install cookiecutter
```

### Generate the package

Generate a new Plone Distribution package by running `Cookiecutter`:

```shell
cookiecutter gh:collective/cookiecutter-plone-distribution
```

And answer the questions:
```
distribution_title [Plone Distribution]: Blog
description [Plone Distribution.]: A Blog using the Plone CMS
github_organization [collective]:
python_package_name [collective.blog]: collective.blog
author [Plone Foundation]: Plone Community
email [collective@plone.org]: borg@plone.org
```

After a while, the folder `collective.blog` will be created, containing the codebase of your Plone Distribution.

### Install the package (local development)

Enter the new folder, and install the codebase:

```shell
cd collective.blog
make build
```

### Lint and Format the codebase

To lint the codebase, use:

```shell
make lint
```

If errors occur, run:

```shell
make format
```

### Testing

We recommend the usage of `pytest` and [pytest-plone](https://pypi.org/project/pytest-plone) to test the package.

The template generator creates a top level folder named `tests` with initial tests. Run them with:

```shell
make test
```
