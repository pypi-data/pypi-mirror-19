============
nagios-audit
============

A Nagios tool for auditing purpose. This tool reads the nagios status file (status.dat) and provides a report of servers and services which needs to be taken care. It reports the servers and services which are not in OK state, notifications disabled, acknowledged and are in scheduled downtime.

Installation
============
::

    pip install nagios-audit


Usage
=====
::

    nagios-audit --input_file ~/Downloads/status.dat  --output_file ~/tmp/test.csv
