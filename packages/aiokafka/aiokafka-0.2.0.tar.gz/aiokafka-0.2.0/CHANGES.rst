CHANGES
--------

0.2.0 (2016-12-18)
^^^^^^^^^^^^^^^^^^

* Added SSL support. (PR #81 by Drizzt1991)
* Fixed UnknownTopicOrPartitionError error on first message for autocreated topic (PR #96 by fabregas)
* Fixed `next_record` recursion (PR #94 by fabregas)
* Fixed Heartbeat fail if no consumers (PR #92 by fabregas)
* Added docs addressing kafka-python and aiokafka differences (PR #70 by Drizzt1991)
* Added `max_poll_records` option for Consumer (PR #72 by Drizzt1991)
* Fix kafka-python typos in docs (PR #69 by jeffwidman)
* Topics and partitions are now randomized on each Fetch request (PR #66 by Drizzt1991)


0.1.4 (2016-11-07)
^^^^^^^^^^^^^^^^^^

* Bumped kafka-python version to 1.3.1 and Kafka to 0.10.1.0.
* Fixed auto version detection, to correctly handle 0.10.0.0 version
* Updated Fetch and Produce requests to use v2 with v0.10.0 message format on brokers.
  This allows a ``timestamp`` to be associated with messages.
* Changed lz4 compression framing, as it was changed due to KIP-57 in new message format.
* Minor refactorings

Big thanks to @fabregas for the hard work on this release (PR #60)


0.1.3 (2016-10-18)
^^^^^^^^^^^^^^^^^^

* Fixed bug with infinite loop on heartbeats with autocommit=True. #44
* Bumped kafka-python to version 1.1.1
* Fixed docker test runner with multiple interfaces
* Minor documentation fixes


0.1.2 (2016-04-30)
^^^^^^^^^^^^^^^^^^

* Added Python3.5 usage example to docs
* Don't raise retriable exceptions in 3.5's async for iterator
* Fix Cancellation issue with producer's `send_and_wait` method


0.1.1 (2016-04-15)
^^^^^^^^^^^^^^^^^^

* Fix packaging issues. Removed unneded files from package.

0.1.0 (2016-04-15)
^^^^^^^^^^^^^^^^^^

Initial release

Added full support for Kafka 9.0. Older Kafka versions are not tested.
