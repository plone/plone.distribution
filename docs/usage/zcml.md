# Registration

The common way to register a new distribution is via ZCML.

First, you need to include `plone.distribution` as a dependency of your package by adding the following snippet to your {file}`configure.zcml` as shown below.

```xml
  <include package="plone.distribution" />
```

Then declare the distributions included in your package using the `plone:distribution` configuration as shown below.

```xml
  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      />
```


(zcml-options-label)=

## Options

| attribute | description | default value | required |
|--|--|--|--|
| `name` | Identifier of the distribution |  | yes |
| `title` | Friendly name of the distribution |  | yes |
| `description` | An explanation of the distribution |  | no |
| `directory` | Distribution directory | distributions/`<name>` | no |
| `pre_handler` | Callable function to process answers before site creation |  | no |
| `handler` | Callable function used by `plone.distribution` to handle site creation |  | no |
| `post_handler` | Callable function used to make adjustments after site is created  |  | no |
| `headless` | Flag indicating if this is a headless distribution of Plone  | true | no |

## Examples

This section provides examples of this package being used in production.
They may serve as useful references for developing your own distribution.

### [`collective.ploneintranet`](https://github.com/collective/collective.ploneintranet/blob/main/src/collective/ploneintranet/distributions.zcml)

This example is a distribution with a specific `post_handler` that is used to configure authentication in the newly created site.

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

This is an example distribution with the following.

* `pre_handler` used to process answers and populate `title`, `description`, and `default_language`
* `post_handler` used to configure registry options in the newly created site

```xml
  <plone:distribution
      name="portal_leg"
      title="PortalBrasil.leg"
      description="Uma distribuição Plone para instituições do legislativo."
      pre_handler=".handlers.pre_handler"
      post_handler=".handlers.post_handler"
      />
```
