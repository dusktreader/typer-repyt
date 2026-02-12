# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## v0.9.0 - 2026-02-11
- Switched build backend from hatchling to uv_build
- Replaced mypy and basedpyright with ty for type checking
- Removed upper bounds from dependency version specifiers
- Updated Makefile


## v0.8.1 - 2025-05-22
- Moved `metavar` into ParamDef


## v0.8.0 - 2025-05-20
- Added parser kwarg for pydantic args/opts

## v0.7.2 - 2025-05-16
- Fixed python version to allow 3.12 through 3.14


## v0.7.1 - 2025-05-12
- Made sure args were added to the namespace to avoid NameErrors for enum types


## v0.7.0 - 2025-05-01
- Pared back functionality to _just_ the `build_command` feature
- All other features are being ported to the new `typerspace` package


## v0.6.0 - 2025-04-25
- Completed error handling including:
 - the `@handle_errors` decorator
 - adding `@handle_errors` to cache and settings commands
- Added documentation for error handling
- Added a demo for error handling


## v0.5.0 - 2025-04-24
- Completed the `cache` functionality including:
  - the `@attach_cache` decorator
  - the `get_manager()` function
  - the `CacheManager`
  - The various `cache` subcommands
  - the `add_cach_subcommand()` function
- Added documentation for the `cache` feature
- Added demos for the `cache` feature


## v0.4.1 - 2025-04-23
- Some small enhancements to the demo


## v0.4.0 - 2025-04-23
- Improved the `get_settings()` function to take a type hint to avoid casting


## v0.3.0 - 2025-04-23
- Completed `settings` functionality including:
  - the `@attach_settings` decorator
  - the `get_settings()` function
  - the `SettingsManager`
  - the various `settings` subcommands
  - the `add_settings_subcommand()` function
- Added documentation for the `settings` feature
- Added demos for the `settings`  and `build_command` features


## v0.2.0 - 2025-04-17
- Renamed the project to `typer-repyt`
- Completed `build_command` function
- Added documentation for the `build_command` feature
- Added examples of the `build_command` feature
- Added a logo


## v0.1.0 - 2025-04-15
- Generated project from template
