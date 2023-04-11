# docker-pyproxy3
TCP Relay/Mirror/Forwarding server 

### A. Use python script
```
usage: pyproxy3.py [-h] port dest1_host dest2_host

TCP Relay/Mirror/Forwarding server

positional arguments:
  port        Listen on `port` for incoming traffic to be duplicated
  dest1_host  Relay traffic to Hostname of destination 1
  dest2_host  Relay traffic to Hostname of destination 2

optional arguments:
  -h, --help  show this help message and exit

```

### B. Use Docker Composer
- Run in containers.
```
  $ git https://github.com/pvrmza/docker-pyproxy3.git
  $ cd docker-pyproxy3
  $ vi env (edit port and destinaton)
  $ docker-compose --env-file ./env up -d
```
