[HORNET](https://github.com/gohornet/hornet) is a lightweight alternative to IOTA's fullnode software “[IRI](https://github.com/iotaledger/iri)”.
The main advantage is that it compiles to native code and does not need a Java Virtual Machine, which considerably decreases the amount of needed resources while significantly increasing the performance.
This way, HORNET is easier to install and runs on low-end devices.

This repository contains tools that help managing HORNET nodes.

It's designed to work with [nfpm](https://github.com/goreleaser/nfpm) CLI tool to create a `.deb.` package.

# Install

Tested on Ubuntu 18.04.

1. install nfpm into Ubuntu:
```
$ wget https://github.com/goreleaser/nfpm/releases/download/v1.2.1/nfpm_amd64.deb
$ sudo dpkg -i nfpm_amd64.deb
```

2. create hornetctl package:
```
$ git clone https://github.com/honeycombOS/hornetctl
$ cd hornetctl
$ export HORNETCTL_VERSION=0.1
$ nfpm pkg -t hornetctl_0.1_all.deb
```

3. Install hornetctl package into Ubuntu:
```
$ sudo dpkg -i hornetctl_0.1_all.deb
```

# Usage:
```
$ hornetctl -h
Usage: hornetctl [options]

Options:
  -h, --help  show this help message and exit
  --start     Start Hornet Systemd Service. (default)
  --stop      Stop Hornet Systemd Service.
```

```
$ hornet_dashboard -h
Usage: hornet_dashboard [options]

Options:
  -h, --help  show this help message and exit
  --off       Disable Hornet Dashboard.
  --on        Enable Hornet Dashboard (default).
```

```
$ hornet_network -h
Usage: hornet_network [options]

Options:
  -h, --help     show this help message and exit
  -c, --comnet   Set Hornet Service to ComNet.
  -m, --mainnet  Set Hornet Service to MainNet (default).
```

```
$ hornet_neighbors -h
usage: hornet_neighbors [-h] [--debug] [--neighbors NEIGHBORS]
                        [--remove-reverse] (--remove | --add | --list)
                        [--file FILE] [--host HOST] [--timeout TIMEOUT]
                        [--hornet] [--version] [--api-version API_VERSION]
hornet_neighbors: error: one of the arguments --remove/-r --add/-a --list/-l is required
```
