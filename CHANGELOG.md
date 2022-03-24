# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- Note: Update the `Unreleased link` after adding a new release -->

## [Unreleased](https://github.com/appsembler/tahoe-sites/compare/v0.1.6...HEAD)

## [0.1.6](https://github.com/appsembler/tahoe-sites/compare/v0.1.5...v0.1.6) - 2022-03-24
 - Add more APIs to support edx-platform smoothly
 - Add two temporary APIs (start with the name `deprecated_`) which should be removed soon 

## [0.1.5](https://github.com/appsembler/tahoe-sites/compare/v0.1.4...v0.1.5) - 2022-03-08
 - Change behaviour of get_organization_for_user
 - Fix local tox not setting the correct pip Version 

## [0.1.4](https://github.com/appsembler/tahoe-sites/compare/v0.1.3...v0.1.4) - 2022-03-03
 - Fixing a syntax error in 0.1.3 that crashed the package
 - Removing migration file that deletes `is_active` field
 - Removing `assert` from production code 

## [0.1.3](https://github.com/appsembler/tahoe-sites/compare/v0.1.2...v0.1.3) - 2022-03-03
 - Remove is_active_admin_on_any_organization API
 - Add more APIs for getting current Site
 - Add get_organization_by_course API
 - cleaner ci.yml github actions matrix
 - Remove is_active Field and rely on User.is_active
 - Move Backends to this repo

## [0.1.2](https://github.com/appsembler/tahoe-sites/compare/v0.1.1...v0.1.2) - 2022-02-24
 - Move get_current_organization to this package
 - New API helper update_admin_role_in_organization
 - One Organization Per User
 - New API Helper add_user_to_organization

## [0.1.1](https://github.com/appsembler/tahoe-sites/compare/ef43ca91543432335e6ddb9b26cab11059811f64...v0.1.1) - 2022-02-10
 - First release to be publish to PyPi
 - Most of the Python API helpers are ready to be used
 - starting changelog

## 0.1
 - Initial GitHub repo. Not released to PyPi.

