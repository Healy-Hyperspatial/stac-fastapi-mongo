# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0/).

## [Unreleased]

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

[Unreleased]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.0.1...main>
[v3.0.1]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/compare/v3.0.0...v3.0.1>
[v3.0.0]: <https://github.com/Healy-Hyperspatial/stac-fastapi-mongo/tree/v3.0.0>
