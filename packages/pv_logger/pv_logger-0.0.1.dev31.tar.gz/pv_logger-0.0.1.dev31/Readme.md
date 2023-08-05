# Python PV Logger

Logging of photovoltaic inverters
* to local cache (sqlite)
* to InfluxDB (can be remote over ssh)

## Kaco over RS485

```
pip install pv_logger
```

create a config file `config.yaml`:
```
archive_older_than_days: 30
# path to sqlite database
# change to file for permanent storage (!!)
engine: "sqlite:///:memory:"
influx:
  dbname: pv-nodes
  host: localhost
  password: no-need
  port: 8086
  user: no-need
tags:
  host: testhost.de
  region: europe
port: "/dev/ttyUSB*"
inverter_ids: [1,2,3]
read_interval_seconds: 10
...
[not up to date, check config.yaml as example]
```

run logger in folder where `config.yaml` is located
```
kaco_logger
```

## SMA Sunny Boy over RS485

TODO

## SMA Sunny Mini Central over Bluetooth

TODO

## Additional Statistics
- uptime (TODO)
- last request status
- reboot reason (TODO)
- awk '/MemFree/{print $2}' /proc/meminfo (TODO)

## Watchdog Manager

Implemenetd in all loggers, some minor differences.

#### Registered Checks:
- no internet for some amount of time
- no port (ttyUSB) found for some amount of time

#### Check for Reboot:
- check need for reboot
    - regularly check a function or result set by user
    - register function to check and how often it has to fail in a row
- check if uptime enough
- log reboot reason
- reboot


## TODO
- now uptime is used everywhere, so we do not rely on the real time, which
  is hard to get on a read only system
- WARNING: sometimes a test fails, as uptime is not very precise in sub-second
  timing

- issues with "hang" loop, program does not seem to do anything, e.g. on pv-strass: (date ok, script still running, but no new logs... strange!)
```
pi@raspberrypi:~ $ date
Sat Dec 10 12:25:43 UTC 2016
pi@raspberrypi:~ $ date^C
pi@raspberrypi:~ $  sudo journalctl -u pv-logger -l -r 
-- Logs begin at Thu 2016-11-10 10:57:05 UTC, end at Sat 2016-12-10 11:52:16 UTC. --
Dec 10 11:52:16 raspberrypi python[738]: INFO:urllib3.connectionpool:Resetting dropped connection: localhost
Dec 10 11:51:21 raspberrypi python[738]: /lib/python2.7/dist-packages/kacors485/kacors485.py", line 249, in readInverterAndParse\n    raise Exception(\'Could not get an answer from the inverter 
Dec 10 11:51:21 raspberrypi python[738]: in readInverterAndParse\n    raise Exception(\'Could not get an answer from the inverter number {}; Answer: {:s}\'.format(inverterNumber, repr(answers)))
Dec 10 11:51:21 raspberrypi python[738]: answer from the inverter number {}; Answer: {:s}\'.format(inverterNumber, repr(answers)))\nException: Could not get an answer from the inverter number 1;
Dec 10 11:51:21 raspberrypi python[738]: erNumber, repr(answers)))\nException: Could not get an answer from the inverter number 1; Answer: {\'#010\\r\\n\': \'\', \'#013\\r\\n\': \'\'}\n'}, 'meas
Dec 10 11:51:21 raspberrypi python[738]: om the inverter number 1; Answer: {\'#010\\r\\n\': \'\', \'#013\\r\\n\': \'\'}\n'}, 'measurement': u'communication', 'tags': {u'pv-location': u'pv_strass
Dec 10 11:51:21 raspberrypi python[738]: \\r\\n\': \'\'}\n'}, 'measurement': u'communication', 'tags': {u'pv-location': u'pv_strass'}, 'time': '2016-12-03T19:22:29.603194'}, {'fields': {u'uptime
Dec 10 11:51:21 raspberrypi python[738]: 'pv-location': u'pv_strass'}, 'time': '2016-12-03T19:20:24.690644'}, {'fields': {u'uptime_node': 70779.57, u'uptime_app': 2017303.496516, u'ram_free_kb':
Dec 10 11:51:21 raspberrypi python[738]: 39'}, {'fields': {u'uptime_node': 70654.64, u'uptime_app': 2017178.571738, u'ram_free_kb': 725032.0}, 'measurement': u'system', 'tags': {u'pv-location': 
Dec 10 11:51:21 raspberrypi python[738]: 53.622717, u'ram_free_kb': 725216.0}, 'measurement': u'system', 'tags': {u'pv-location': u'pv_strass'}, 'time': '2016-12-03T19:16:14.816975'}, {'fields':
Dec 10 11:51:21 raspberrypi python[738]: 'tags': {u'pv-location': u'pv_strass'}, 'time': '2016-12-03T19:14:09.877641'}, {'fields': {u'last_request_status': u'error', u'error_msg': u'Traceback (m
Dec 10 11:51:21 raspberrypi python[738]: 2:05.010469'}, {'fields': {u'last_request_status': u'error', u'error_msg': u'Traceback (most recent call last):\n  File "/usr/local/lib/python2.7/dist-pa
Dec 10 11:51:21 raspberrypi python[738]: rror_msg': u'Traceback (most recent call last):\n  File "/usr/local/lib/python2.7/dist-packages/pv_logger/kaco.py", line 30, in read_all_inverter\n    da
Dec 10 11:51:21 raspberrypi python[738]: cal/lib/python2.7/dist-packages/pv_logger/kaco.py", line 30, in read_all_inverter\n    data = read_inverter(kaco, i)\n  File "/usr/local/lib/python2.7/di
Dec 10 11:51:21 raspberrypi python[738]: read_all_inverter\n    data = read_inverter(kaco, i)\n  File "/usr/local/lib/python2.7/dist-packages/pv_logger/kaco.py", line 11, in read_inverter\n    i
Dec 10 11:51:21 raspberrypi python[738]: /usr/local/lib/python2.7/dist-packages/pv_logger/kaco.py", line 11, in read_inverter\n    inv_data = kaco.readInverterAndParse(int(inverter_id))\n  File 
Dec 10 11:51:21 raspberrypi python[738]: 11, in read_inverter\n    inv_data = kaco.readInverterAndParse(int(inverter_id))\n  File "/usr/local/lib/python2.7/dist-packages/kacors485/kacors485.py",
Dec 10 11:51:21 raspberrypi python[738]: (int(inverter_id))\n  File "/usr/local/lib/python2.7/dist-packages/kacors485/kacors485.py", line 249, in readInverterAndParse\n    raise Exception(\'Coul
Dec 10 11:51:21 raspberrypi python[738]: ges/kaco
```
