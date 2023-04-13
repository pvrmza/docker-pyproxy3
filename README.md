# docker-tcptee
TCPtee - mirrors TCP traffic received on a port to two remote destinations

### A. Use python script
```
usage: tcptee.py [-h] port dest1 dest2

TCPtee - a Relay/Mirror/Forwarding server

positional arguments:
  port        Listen on `port` for incoming traffic to be duplicated
  dest1       Relay traffic to Hostname of destination 1 (IP:port)
  dest2       Relay traffic to Hostname of destination 2 (IP:port)

optional arguments:
  -h, --help  show this help message and exit

```

### B. Use Docker Composer
- Run in containers.
```
  $ git https://github.com/pvrmza/docker-tcptee.git
  $ cd docker-tcptee
  $ edit env file (edit port and destinaton)
  $ docker-compose --env-file ./env up -d
```
