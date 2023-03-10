# Usage

```{toctree}
:maxdepth: 1
:hidden: true

package-structure
code-examples
```

A Plone distribution is a Python package that can be installed by `pip` and follows certain conventions.

## Create a new Plone distribution

The Plone community provides a [Cookiecutter](https://www.cookiecutter.io/) template to generate new Plone distribution packages: [`cookiecutter-plone-distribution`](https://github.com/collective/cookiecutter-plone-distribution).

This template is under active development.
It will probably change its structure until a stable release of `plone.distribution` is made.

### Pre-requisites

To use the template, install `Cookiecutter` via the command line.

```shell
pip install cookiecutter
```

### Generate the package

Generate a new Plone distribution package by running the cookiecutter.

```shell
cookiecutter gh:collective/cookiecutter-plone-distribution
```

Answer the questions, replacing the following with your desired options.

```console
distribution_title [Plone Distribution]: Blog
description [Plone Distribution.]: A Blog using the Plone CMS
github_organization [collective]:
python_package_name [collective.blog]: collective.blog
author [Plone Foundation]: Plone Community
email [collective@plone.org]: borg@plone.org
```

After a while, the folder `collective.blog` (or your chosen name) will be created, containing the code base of your Plone distribution.

### Install the package for local development

Enter the new folder, and install the code base.

```shell
cd collective.blog
make build
```

### Lint and format the code base

Lint the code base.

```shell
make lint
```

If errors occur, then run the following command.

```shell
make format
```

### Testing

We recommend [`pytest`](https://pypi.org/project/pytest/) and [`pytest-plone`](https://pypi.org/project/pytest-plone) to test the package.

The template generator creates a top level folder named `tests` with initial tests.
To run the tests, use the following command.

```shell
make test
```
