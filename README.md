<p align="center">
    <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-logo.png">
</p>

<h1 align="center">
  Plone Distributions
</h1>

Package supporting the (easy) implementation of a Plone Distribution.

## What is a Plone Distribution

A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations. It is a convenient way to get a specific type of website up and running quickly, as the distribution includes everything needed to run that type of site.

Examples of Plone distributions include:

* [SENAITE](https://www.senaite.com)
* [Quaive](https://quaivecloud.com/)
* [Portal Modelo](https://www.interlegis.leg.br/produtos-servicos/portal-modelo/)
* [Portal Padrão](https://identidade-digital-de-governo-plone.readthedocs.io/en/latest/)

### Similar Concept in Other CMS

* Drupal: Drupal has distributions for blogs, e-commerce sites, and intranet portals.

* WordPress: WordPress has a similar concept in the form of "WordPress Multisite," which allows users to run multiple websites from a single installation of WordPress.

* Joomla: Joomla has a similar concept in the form of "Joomla Templates," which are pre-designed templates for Joomla websites.

* TYPO3: TYPO3 has a similar concept in the form of "TYPO3 Distributions," which are pre-configured installations of TYPO3 for specific types of websites.

## Creating a new Distribution

First of all, a Plone Distribution is a Python Package that can be installed by `pip`.

### `setup.py`
The package will follow some conventions, to make it "discoverable" by others.

In `setup.py`, always add the correct Trove Classifiers:

```python
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Distribution",
```

and also require `plone.distribution` to be available:

```python
    install_requires=[
        "Plone",
        "setuptools",
        "plone.distribution",
    ],
```

### `configure.zcml`

In your main `configure.zcml`, make sure to have the `plone` xml namespace declared:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    >
```

And also include `plone.distribution`:

```xml
  <include package="plone.distribution" />
```

Then declare the distributions included in your package:

```xml

  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      />

```

The registered distribution will configure a Personal Blog, with some default content.

### distribution folder

A convention is to use the `distributions/<distribution_name>`folder in the root of your package to organize your distribution configuration.

In that folder, you will need to provide:

### `image.png`

A 1080x768 image of your distribution. It could be the default page of a new site, your logo, or any other way of representing this distribution.

### `profiles.json`

A `JSON` file with the GenericSetup profiles that are used by your distribution during installation.

This file needs to contain two keys:

* **base**: List of profiles installed in every new site using this distribution.

* **content**: List of profiles installed when the user decides to create a site with example content.

The configuration for a new Volto site is:

```json
{
  "base": [
    "plone.app.contenttypes:default",
    "plone.app.caching:default",
    "plonetheme.barceloneta:default",
    "plone.volto:default"
  ],
  "content": [
    "plone.volto:default-homepage"
  ]
}
```

### `schema.json`

In case you require additional input from the user during site creation, you can customize the form using the `schema.json` file.

The file should contain two keys:

* **schema**: A JSON Schema definition.
* **uischema**: A [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/docs/) configuration to modify how the form is displayed.

The **schema** should have at least the following keys:

* site_id
* title
* description
* default_language
* portal_timezone
* setup_content

The `schema.json` used for the default site creation is:

```json
{
  "schema": {
    "title": "Create a Plone site",
    "description": "Adds a new Plone content management system site to the underlying application server.",
    "type": "object",
    "required": [
      "site_id",
      "title"
    ],
    "properties": {
      "site_id": {
        "type": "string",
        "title": "Path Identifier",
        "default": "Plone",
        "description": "The ID of the site. No special characters or spaces are allowed. This ends up as part of the URL unless hidden by an upstream web server."
      },
      "title": {
        "type": "string",
        "title": "Title",
        "default": "Site",
        "description": "A short title for the site. This will be shown as part of the title of the browser window on each page."
      },
      "description": {
        "type": "string",
        "title": "Site Description",
        "default": "A Plone Site"
      },
      "default_language": {"$ref": "#/definitions/languages"},
      "portal_timezone": {"$ref": "#/definitions/timezones"},
      "setup_content": {
        "type": "boolean",
        "title": "Create Content",
        "description": "Should example content be added during site creation?",
        "default": false
      }
    }
  },
  "uischema": {
  }
}

```

**Important**
You probably noticed the entries for
default_language:

```
{"$ref": "#/definitions/languages"}
```
and portal_timezone:

```
{"$ref": "#/definitions/timezones"}
```

Both definitions are added in runtime by `plone.distribution` to provide a list of languages and timezones available on the installation.

### `content` folder

**WIP**: Folder containing json data exported by `collective.exportimport`

## Advanced Usage

### Hiding Distributions

By default, `plone.distribution` ships with two ready-to-use distributions:

* **default**: Plone Site (Volto frontend)
* **classic**: Plone Site (Classic UI)

If you want to limit your users option to select a distribution, it is possible to set the environment variable `ALLOWED_DISTRIBUTIONS` with fewer options:

```shell
ALLOWED_DISTRIBUTIONS=default
```


## This project is supported by

<p align="left">
    <a href="https://plone.org/foundation/">
      <img alt="Plone Logo" width="200px" src="https://raw.githubusercontent.com/plone/.github/main/plone-foundation.png">
    </a>
</p>

## License
The project is licensed under the GPLv2.
