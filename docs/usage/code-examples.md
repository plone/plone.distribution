
(chapter-code-examples)=

# Code examples

This chapter provides code examples to use with `plone.distribution`.

## `api.distribution`

This section describes how to interface with the `distribution` module.

(api-distribution-get_registry-example)=

### Get distribution registry

To get the distribution registry, the utility which holds all available distributions in an installation, use the method {meth}`api.distribution.get_registry`.

```python
from plone.distribution.api import distribution as dist_api
registry = dist_api.get_registry()
```

(api-distribution-get_distributions-example)=

### Get all registered distributions

Return a list of all distributions using the method {meth}`api.distribution.get_distributions`.

```python
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution

distributions = dist_api.get_distributions()

assert isinstance(distributions, list)
assert isinstance(distributions[0], Distribution)
```

(api-distribution-get-example)=

### Get one distribution

Get one distribution by its name with the method {meth}`api.distribution.get`.

```python
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution

distribution = dist_api.get(name="default")

assert isinstance(distribution, Distribution)
assert distribution.title == "Plone Site"
```

## `api.site`

This section describes how to interface with the `site` module.

(api-site-get_sites-example)=

### Get the list of all sites

To get a list of all Plone sites, pass the application root to the method {meth}`api.site.get_sites`.

```python
from plone.distribution.api import site as site_api


sites = site_api.get_sites(app)
```


(api-site-get_creation_report-example)=

### Get creation report for a site

To get a report of the creation of the site use the method {meth}`api.site.get_creation_report`.

```python
from plone.distribution.api import site as site_api

site = app.Plone
report = site_api.get_creation_report(site)
```

(api-site-create-example)=

### Create a new site

Create a new Plone site using one of the available distributions using the method {meth}`api.site.create`.

```python
from plone.distribution.api import site as site_api

distribution_name = "default"
answers = {
    "site_id": "Plone",
    "title": "My Plone Site",
    "description": "A new Plone site using the default distribution",
    "default_language": "en",
    "portal_timezone": "UTC",
}

new_site = site_api.create(app, distribution_name, answers)
```
