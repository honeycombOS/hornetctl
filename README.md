[HORNET](https://github.com/gohornet/hornet) is a lightweight alternative to IOTA's fullnode software “[IRI](https://github.com/iotaledger/iri)”.
The main advantage is that it compiles to native code and does not need a Java Virtual Machine, which considerably decreases the amount of needed resources while significantly increasing the performance.
This way, HORNET is easier to install and runs on low-end devices.

This repository contains tools that help managing HORNET nodes.

It's designed to work with [nfpm](https://github.com/goreleaser/nfpm) CLI tool to create a `.deb.` package.

```
export HORNETCTL_VERSION=0.1
nfpm pkg -t goshimmerctl_0.1_all.deb
```

