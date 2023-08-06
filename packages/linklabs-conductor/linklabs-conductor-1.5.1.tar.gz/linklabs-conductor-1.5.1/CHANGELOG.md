## [1.5.1] - 2017-1-4
### Added
- Added user-settable "on_close" callback for subscriptions

### Changed
- Default UplinkMessage.network_token to None if it's not set in Conductor.

## [1.5.0] - 2016-10-28
### Changed
- Implement __eq__ and others for classes
- Use Conductor's "next page" concept to split large queries into multiple
requests

### Deprecated
- Deprecate get_messages_time_range_chunked, as chunking large queries
is now handled automatically.

## [1.4.0] - 2016-9-19
### Added
- Initial release. Includes functionality for querying data and metadata
for uplink messages from app tokens, network tokens, gateways, modules,
and accounts.
- Can send downlink messages to modules (unicast) and app tokens (multicast)
- Can query for status of downlink messages and cancel downlink messages
- Can get data about subjects through the common _data attribute
