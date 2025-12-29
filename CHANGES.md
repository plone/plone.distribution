# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 4.0.0a2 (2025-12-29)


### Bug fixes:

- Remove deprecated `plone.volto:default-homepage` profile from `README.md` recommendations. @Thanush-03 #99


### Documentation:

- Fix Sphinx build. @stevepiercy #133
- Remove duplicate documentation from `README.md` and link to authoritative source. @stevepiercy #136

## 4.0.0a1 (2025-11-26)


### Breaking changes:

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.
  Support only Plone 6.2 and Python 3.10+. #3928

## 3.2.1 (2025-09-05)


### Bug fixes:

- Fix frontend resource paths to work properly with VHM. @wesleybl #98

## 3.2.0 (2025-06-18)


### New features:

- Support specifying a base GenericSetup profile during distribution registration. @ericof #116


### Bug fixes:

- Set the site hook when accessing the migration tool for a site. @ericof #117
- Fix POSKeyError in tests by adding a transaction.savepoint after importing default content with plone.exportimport. @ericof #119


### Internal:

- Add configuration for ruff as code formatter. @ericof 
- Update .vscode settings. @ericof 
- Update config files using plone.meta @ericof 

## 3.1.2 (2025-04-05)


### New features:

- Add attribute `package` to `plone.distribution.core.Distribution` to store which package registered a specific distribution. @ericof #114

## 3.1.1 (2025-03-11)


### Bug fixes:

- frontend: relative backend requests @lyralemos #98
- Replace `pkg_resources` with `importlib.metadata` @gforcada #4126

## 3.1.0 (2025-02-06)


### New features:

- frontend: show id of Plone instance. @ksuess #109

## 3.0.0 (2025-01-29)


### New features:

- Include revisions only when passing `--include-revisions`.  @mauritsvanrees #39


### Bug fixes:

- Fix warning for unclosed file at startup. #4090

## 3.0.0b2 (2024-12-19)


### Bug fixes:

- Fix logic for suggested id for new site.
  It could suggest an id that was already taken.
  @mauritsvanrees #97


### Tests

- Fix test that failed because an extra distribution was found.
  @mauritsvanrees #104

## 3.0.0b1 (2024-11-25)


### Bug fixes:

- Fix bug where launch screen was blank in Chrome. @davisagli #101

## 3.0.0a1 (2024-10-31)


### Breaking changes:

- Move internal classic distribution to plone.classicui [@mauritsvanrees][@ericof] #79


### New features:

- Move internal default distribution to plone.volto [@mauritsvanrees][@ericof] #80


### Internal:

- Clarify RestTraverser code.
  [maurits]

## 2.0.0b1 (2024-05-17)


### New features:

- Redesign the site creation page [@danalvrz] #63

## 2.0.0a1 (2024-05-16)


### Breaking changes:

- plone.distribution is now based on plone.exportimport instead of collective.exportimport.

  There are some backwards-incompatible changes in the export format.
  To convert an existing distribution to the new format, use the following steps:
  1. Create a site from the distribution using plone.distribution 1.0.x
  2. Install plone.distribution 2.0.x
  3. Delete the distribution's `contents/items` folder.
  4. Export the distribution in the new format using the `bin/export-distribution` script.

  @davisagli, @ericof #61


### New features:

- Default distribution: Allow users to upload a logo during site creation [@ericof] #66
- Classic distribution: Allow users to upload a logo during site creation [@ericof] #67
- Remove dependency on Plone package, add dependency on Products.CMFPlone [@ericof] #70


### Bug fixes:

- Get the name of the existing distribution from the report, not the answers [@ericof] #60
- Fix issue with payload for new site creation breaking with certain plone.rest versions [@ericof] #71
- Read profile.json by the pathlib.Path.read_text method to avoid the unclosed file exception [@folix-01] #75


### Internal:

- Update `plone/meta` configuration [@ericof] #73
- Log traceback when creating a site fails [@pbauer] #82
- Bump `plone.exportimport` to 1.0.0a5 [@ericof] #83

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
