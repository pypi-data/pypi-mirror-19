=============================
Change log for gocept.logging
=============================

0.8.1 (2017-01-09)
==================

- Fix `setup.py` to use relative paths.


0.8 (2016-03-17)
================

- Declare compatibility with PyPy and PyPy3.


0.7 (2015-09-29)
================

- Declare Python 3.5 compatibility.


0.6 (2015-09-17)
================

- Declare Python 3.4 compatibility.

- ``ArgumentParser.parse_args()`` now stores the computed log level on the
  ``log_level`` attribute of the return value.

0.5 (2014-02-07)
================

- Allow to change log format for the ``ArgumentParser``


0.4 (2013-09-24)
================

- Handle non-string log messages properly.


0.3 (2013-09-04)
================

- Added sepcialized ``argparse.ArgumentParser`` which enables user to set the
  ``logging`` level by default..


0.2 (2013-08-24)
================

- Add timestamp and hostname to syslog messages,
  this allows plugging SyslogKeyValueFormatter directly into logstash
  without an intermediary syslogd.


0.1 (2013-08-16)
================

- initial release
