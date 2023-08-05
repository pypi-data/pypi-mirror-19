Rancon (aka rancher-consul)
===========================

We use consul as a service discovery mechanism, and a Consul-template / HAProxy combination to route traffic into our services. This python script is a helper to automatically enter Rancher services into Consul based on Rancher label selectors, so they can picked up by the load HAProxy load balancing layer.

This might not be of any use to anybody but me, but I'll make it public anyway because I did not find another solution so I had to write it, and maybe someone else has the same problem.

CHANGELOG
=========

0.11.0
------

Date: 2017-01-03

- FIX: Service tag replacment exception


0.10.0
------

Date: 2017-01-03

- FEATURE: Add "web interface" (basically only for metrics and health check)
- FEATURE: Add health check under /health
- FEATURE: Add prometheus metrics under /metrics
- CHANGE: Deregistration behavior for services which failed registration (was:
  unregister, is now: keep)


0.9.0
-----

Date: 2016-06-15

- CHANGE: convert IDs, tags, names to all lowercase in consul
- CHANGE: do not allow non-url characters in service IDs (basically nothing but [a-z0-9-])


0.8.0
-----

Date: 2016-06-15

- BREAKING: ``-i/--id`` parameter no longer global, moved to ``cleanup_id`` parameter of backend
- CHANGE: output now logging based, so all to stderr, and -vvvv flags possible
- FIX: bug in service lookup in Rancher
- OPEN: https connections


0.7.0
-----

Date: 2016-06-15

- FEATURE: authentication now used
- FIX: bug in service lookup in Rancher
- OPEN: https connections (untested, *might* work)


0.6.1
-----

Date: 2016-06-09

- More verbosity during init process


0.6.0
-----

Date: 2016-06-09

- Unified naming scheme of used environment variables
- Added convenience script "rancon.py"
- Dockerfile fixes
- Doc fixes


0.5.0
-----

Date: 2016-06-07

- Initial PyPI release
- module works, docker setup not tested yet
- documentation unfinished / not present


