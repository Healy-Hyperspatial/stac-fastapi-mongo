# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0/).

## [Unreleased]

### Changed

- Add support for python 3.12. [#22](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/22)
- Updated sfeos core to v3.0.0a0, fixed datetime functionality. [#23](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/23)
- utilities.py/parse_datestring method now returns datetime and not str, otherwise time filtering does not work for MongoDB databases using datetime objects (which is recommended over using date strings). [#32](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/32)

### Fixed

- Added a new index based on collection id and item id to ensure item IDs aren't required to be unique across all collections. [#26](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/26)


## [v3.2.1]

### Changed

- Updated sfeos core to v2.4.1, added new tests from sfeos. [#21](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/21)


## [v3.2.0]

### Changed

- Moved core basic auth logic to stac-fastapi.core. [#19](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/19)
- Updated stac-fastapi.core to v2.4.0. [#19](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/pull/19)


## [v3.1.0]

### Added

- Added option to include Basic Auth. [#12](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/12)

### Changed

- Upgraded stac-fastapi.core to 2.3.0 [#15](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/15)
- Enforced `%Y-%m-%dT%H:%M:%S.%fZ` datetime format on create_item [#15](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/15)
- Queries now convert datetimes to `%Y-%m-%dT%H:%M:%S.%fZ` datetime format [#15](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/15)

### Fixed

- Added skip to basic_auth tests when `BASIC_AUTH` environment variable is not set


## [v3.0.1]

### Added

### Changed

- Removed bulk transactions extension from app.py

### Fixed

- Fixed pagination issue with MongoDB. Fixes [#1](https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/issues/1)


## [v3.0.0]

### Added

### Changed

- New release v3.0.0 using core library from stac-fastapi-elasticsearch-opensearch

### Fixed

----

[Unreleased]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.2.1...main>
[v3.2.1]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.2.0...v3.2.1>
[v3.2.0]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.1.0...v3.2.0>
[v3.1.0]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.0.1...v3.1.0>
[v3.0.1]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.0.0...v3.0.1>
[v3.0.0]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/tree/v3.0.0>
