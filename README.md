[HORNET](https://github.com/gohornet/hornet) is a lightweight alternative to IOTA's fullnode software “[IRI](https://github.com/iotaledger/iri)”.
The main advantage is that it compiles to native code and does not need a Java Virtual Machine, which considerably decreases the amount of needed resources while significantly increasing the performance.
This way, HORNET is easier to install and runs on low-end devices.

This repository contains tools that help managing HORNET nodes.

It's designed to work with [nfpm](https://github.com/goreleaser/nfpm) CLI tool to create a `.deb.` package.

# Python

Tested on Ubuntu 18.04.

1. Install SetupTools:
```
$ sudo apt-get install python3-setuptools
```

2. Clone this repo:
```
$ git clone https://github.com/honeycombOS/hornetctl.git
```

3. Install `hornetctl` Python3 module:
```
$ cd hornetctl
$ sudo python3 setup.py install
``` 

4. Open a Python3 console and try out `hornetctl` API:
```
$ python3
Python 3.6.9 (default, Jul 17 2020, 12:50:27) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import hornetctl
>>> hornetctl.getStatus()
'{\n "version": "HORNET 0.4.2",\n "node": {\n  "status": "inactive"\n },\n "networkType": "mainnet",\n "local": "/var/lib/hornet (SD Card)",\n "dashboardStatus": "disabled",\n "dashboardPort": false\n}'
>>>
```

# NFPM

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
usage: hornetctl [-h] {node,status,network,dashboard,usb,clean,log} ...

positional arguments:
  {node,status,network,dashboard,usb,clean,log}
                        hornetctl subcommands
    node                start/stop node
    status              show node status
    network             set mainnet/comnet
    dashboard           enable/disable dashboard
    usb                 enable/disable USB for db and snapshot
    clean               clean db/snapshot
    log                 show log

optional arguments:
  -h, --help            show this help message and exit

```
