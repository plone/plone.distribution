# Important files and folders

This chapter describes important files and folders generated from the cookiecutter template.

## `setup.py`

The package will follow some conventions, to make it discoverable by others.

In `setup.py`, always add the correct [trove classifiers](https://pypi.org/classifiers/):

```python
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Distribution",
```

Require that `plone.distribution` is available.

```python
    install_requires=[
        "Plone",
        "setuptools",
        "plone.distribution",
    ],
```

## `configure.zcml`

In your main `configure.zcml`, make sure to have the `plone` XML namespace declared.

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    >
```

Include `plone.distribution`.

```xml
  <include package="plone.distribution" />
```

Declare the distributions included in your package.

```xml
  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      />
```

The registered distribution will configure a personal blog with some default content.

## `distributions` folder

By convention use the `distributions/<distribution_name>` folder in the root of your package to organize your distribution configuration.

In that folder, you must provide the following.

### `image.png`

A 1080 pixels wide by 768 pixels tall image of your distribution.
It could be the default page of a new site, your logo, or any other way to represent this distribution.

### `profiles.json`

This is a `JSON` file with the GenericSetup profiles that are used by your distribution during installation.

This file needs to contain two keys.

`base`
:   A list of profiles installed in every new site using this distribution.
`content`
:   A list of profiles installed when the user decides to create a site with example content.

The configuration for a new Volto site is the following.

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

The file should contain two keys.

`schema`
:   A JSON schema definition.
`uischema`
:   A [`react-jsonschema-form`](https://rjsf-team.github.io/react-jsonschema-form/docs/) configuration to modify how the form is displayed.

The schema should have at least the following keys.

* `site_id`
* `title`
* `description`
* `default_language`
* `portal_timezone`
* `setup_content`

The `schema.json` used for the default site creation is the following.

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

````{important}
You probably noticed the entries for `default_language`.

```
{"$ref": "#/definitions/languages"}
```

and `portal_timezone`.

```
{"$ref": "#/definitions/timezones"}
```

Both definitions are added in runtime by `plone.distribution` to provide a list of languages and timezones available on the installation.
````
