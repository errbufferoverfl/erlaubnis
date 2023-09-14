# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2023-09-14

### Added

- A context processor that will preload the `base.html` Jinja template with HTML metadata making it easier to dynamically update templates based on the Flask configuration.

### Changed

- How configuration files are constructed and loaded. They are now split out into individual default, dev, and test files located under the `config` directory.

## 2023-05-13

### Added
- State diagram to README to demonstrate the client authorization state changes.
- Sequence diagram to README to demonstrate the abstract OAuth2.1 protocol flow.
- A CHANGELOG (this file)!

### Removed

- Support for the Implicit grant (`response_type=token`).