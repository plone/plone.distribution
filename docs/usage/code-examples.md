
(chapter-code-examples)=

# Code Examples


## `api.distribution`

(api-distribution-get_registry-example)=

### Get distribution registry

Getting the Distribution Registry, the utility holding all available distributions in an installation, is easy with {meth}`api.distribution.get_registry`.

```python
from plone.distribution.api import distribution as dist_api
registry = dist_api.get_registry()
```

(api-distribution-get_distributions-example)=

### Get all registered distributions

Return a list of all distributions using {meth}`api.distribution.get_distributions`.

```python
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution

distributions = dist_api.get_distributions()

assert isinstance(distributions, list)
assert isinstance(distributions[0], Distribution)
```

(api-distribution-get-example)=

### Get one Distribution

Get one distribution, by name, with {meth}`api.distribution.get`.

```python
from plone.distribution.api import distribution as dist_api
from plone.distribution.core import Distribution

distribution = dist_api.get(name="default")

assert isinstance(distribution, Distribution)
assert distribution.title == "Plone Site"
```

## `api.site`

(api-site-get_sites-example)=

### Get list of all sites

Passing the Application root to the {meth}`api.site.get_sites`, you receive a list of all Plone Sites.

```python
from plone.distribution.api import site as site_api


sites = site_api.get_sites(app)
```

(api-site-create-example)=

### Create a new site

Create a new Plone Site using one of the available distributions using {meth}`api.site.create`:

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
