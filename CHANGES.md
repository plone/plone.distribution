# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0b4 (2024-04-03)


### Bug fixes:

- Fix exporting files.
  [pbauer] #58

## 1.0.0b3 (2024-03-08)


### Bug fixes:

- Fix importing blocks on the site-root.
  [pbauer] #56


### Internal:

- Update configuration files.
  [plone devs] 6e36bcc4

## 1.0.0b2 (2023-10-11)


### New features:

- Remove old blobs before exporting content [@ericof] #34
- Support to new export/import format with one content item per json file [@ericof] #47


## 1.0.0b1 (2023-07-10)


### New features:

- Validate answers payload against jsonschema [@ericof] #38
- Allow distribution to pre process answers before site creation [@ericof] #39
- Override @system from plone.restapi to display distribution information [@ericof] #45


## 1.0.0a9 (2023-06-27)


### Bug fixes:

- Allow setting default_language "default" value [@ericof] #36


## 1.0.0a8 (2023-06-25)


### New features:

- Bump @rjsf/core to version 5.8.2 [@ericof] #35


## 1.0.0a7 (2023-06-24)


### Bug fixes:

- Fix content export to json [@ericof] #33


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
