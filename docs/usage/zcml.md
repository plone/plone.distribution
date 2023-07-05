# Registration

The common way to register a new distribution is via zcml.

First, you need to include `plone.distribution` as dependency of your package by adding the following snippet to your `configure.zcml`:

```xml
  <include package="plone.distribution" />
```

Then declare the distributions included in your package using the `plone:distribution` configuration:

```xml
  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      />
```

## Options

| attribute | description | default value | required |
|--|--|--|--|
| name | Identifier of the distribution |  | ✅ |
| title | Friendly name of the distribution |  | ✅ |
| description | An explanation of the distribution |  |  |
| directory | Distribution directory | distributions/`<name>` |  |
| pre_handler | Callable function to process answers before site creation |  |  |
| handler | Callable function used by `plone.distribution` to handle site creation. |  |  |
| post_handler | Callable function used to make adjustments after site is created  |  |  |

## Examples

### [`collective.ploneintranet`](https://github.com/collective/collective.ploneintranet/blob/main/src/collective/ploneintranet/distributions.zcml)

Distribution with a specific post_handler used to configure authentication in the newly created site:

```xml
  <plone:distribution
      name="intranet-volto"
      title="Plone Intranet (Volto UI)"
      description="Adds a new Plone content management system intranet using Volto UI."
      directory="distributions/volto"
      post_handler=".handler.post_handler"
      />
```

### [`plonegovbr.portal_leg`](https://github.com/plonegovbr/plonegovbr.portal_leg/blob/main/src/plonegovbr/portal_leg/distributions.zcml)

Distribution with:

* pre_handler used to process answers and populate `title`, `description`, `default_language`
* post_handler used to configure registry options in the newly created site

```xml
  <plone:distribution
      name="portal_leg"
      title="PortalBrasil.leg"
      description="Uma distribuição Plone para instituições do legislativo."
      pre_handler=".handlers.pre_handler"
      post_handler=".handlers.post_handler"
      />
```
