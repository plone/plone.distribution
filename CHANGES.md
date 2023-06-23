# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0a6 (2023-06-23)


### New features:

- Improve support for testing distributions [@ericof] #24
- Allow export only for distributions still in development [@ericof] #28
- Create a report for Plone sites created from a distribution [@ericof] #30
- Clean up exported content to remove references to portal.absolute_url() [@ericof] #32


### Bug fixes:

- Content language should be allowed in portal configuration [@ericof] #23


### Internal:

- Update configuration files.
  [plone devs] 047ec50d, 55bda5c9, d7e9e748


## 1.0.0a5 (2023-05-18)


### Bug fixes:

- Import did not import any steps except content and portal. [pbauer] #22


## 1.0.0a4 (2023-05-18)


### New features:

- Increase test coverage.
  [ericof] #12
- Implement JSON import of content [pbauer] #13
- Use mxdev.
  [ericof] #18
- Implement default content for default and classic distributions as JSON.
  [ericof] #20


## 1.0.0a3 (2023-02-08)


### Bug fixes:

- Fix Basic Authentication for Chrome [@ericof] #10


## 1.0.0a2 (2023-02-08)


### New features:

- Change overview page favicon to use Plone logo [@ericof] #7
- Set content creation on `default` and `classic` distributions to be default. [@ericof] #9


### Bug fixes:

- Use [ajv8](https://rjsf-team.github.io/react-jsonschema-form/docs/usage/validation#ajvclass) with Ajv2019 class validator to fix `function nested too deeply` on Firefox [@ericof] #4
- Handle authentication when /acl_users does not support cookie extraction [@ericof] #6


## 1.0.0a1 (2023-02-08)


### New features:

- Initial implementation of plone.distribution [@ericof] #1


## 1.0.0 (Unreleased)
