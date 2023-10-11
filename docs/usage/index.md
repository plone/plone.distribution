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

To use the template, install `pipx` via the command line.

```shell
pip install pipx
```

### Generate the package

Generate a new Plone distribution package by running the cookiecutter.

```shell
pipx run cookiecutter gh:collective/cookiecutter-plone-distribution
```

Answer the questions, replacing the following with your desired options.

```console
Project details
--------------------------------------------------------------------------------

  [1/9] Distribution Title (My Plone Distribution): Blog
  [2/9] A short description of your distribution (A new Plone Distribution): A Blog using the Plone CMS
  [3/9] Is this a headless distribution?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 1
  [4/9] Author (Plone Community):
  [5/9] Author E-mail (collective@plone.org):
  [6/9] GitHub Username or Organization (collective):
  [7/9] Python package name (collective.blog):
  [8/9] Default Language
    1 - English
    2 - Deutsch
    3 - Español
    4 - Português (Brasil)
    5 - Nederlands
    6 - Suomi
    Choose from [1/2/3/4/5/6] (1):
  [9/9] Add example features (Profiles, Vocabularies)?
    1 - No
    2 - Yes
    Choose from [1/2] (1):
```

After a while, the folder `collective.blog` (or your chosen name) will be created, containing the code base of your Plone distribution.

### Install the package for local development

Enter the new folder, and install the code base.

```shell
cd collective.blog
make install
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
