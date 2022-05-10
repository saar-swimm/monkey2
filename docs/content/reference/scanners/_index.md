---
title: "Scanners"
date: 2020-07-14T08:43:12+03:00
draft: false
weight: 20
pre: '<i class="fas fa-network-wired"></i> '
tags: ["reference"]
---

The Infection Monkey agent takes two steps before attempting to exploit a victim, scanning and fingerprinting. It's possible to customize both steps in the configuration files.

## Scanning

Currently there are two scanners, [`PingScanner`][ping-scanner] and [`TcpScanner`][tcp-scanner], both inheriting from [`HostScanner`][host-scanner].

The sole interface required is the `is_host_alive` interface, which needs to return True/False.

[`TcpScanner`][tcp-scanner] is the default scanner. It checks for open ports based on the `tcp_target_ports` configuration setting.

[`PingScanner`][ping-scanner] sends a ping message using the host OS utility `ping.`

## Fingerprinting

Fingerprinters are modules that collect server information from a specific victim. They inherit from the [`HostFinger`][host-finger] class and are listed under the `finger_classes` configuration option.

The currently implemented Fingerprint modules are:

1. [`SMBFinger`][smb-finger] - Fingerprints target machines over SMB and extracts the computer name and OS version.
2. [`SSHFinger`][ssh-finger] - Fingerprints target machines over SSH (port 22) and extracts the computer version and SSH banner.
3. [`PingScanner`][ping-scanner] - Fingerprints target machine's TTL to differentiate between Linux and Windows hosts.
4. [`HTTPFinger`][http-finger] - Detects HTTP/HTTPS services, using the ports listed in `HTTP_PORTS` in the configuration, will return the server type and if it supports SSL.
5. [`ElasticFinger`][elastic-finger] - Fingerprints ElasticSearch (port 9200) and will extract the cluster name, node name and node version.

## Adding a scanner/fingerprinter

To add a new scanner/fingerprinter, create a new class that inherits from [`HostScanner`][host-scanner] or [`HostFinger`][host-finger] (depending on the interface). The class should be under the network module and imported under [`network/__init__.py`](https://github.com/guardicore/monkey/blob/master/monkey/infection_monkey/network/__init__.py).

To use the new scanner/fingerprinter by default, modify [`infection_monkey/config.py`](https://github.com/guardicore/monkey/blob/master/monkey/infection_monkey/config.py) to add references to the new class.

At this point, the Infection Monkey knows how to use the new scanner/fingerprinter but to make it easy to use, the UI needs to be updated. The relevant UI file is [`monkey_island/cc/services/config.py`](https://github.com/guardicore/monkey/blob/master/monkey/monkey_island/cc/services/config.py).

 [elastic-finger]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/elasticfinger.py
 [http-finger]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/httpfinger.py
 [host-finger]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/__init__.py
 [host-scanner]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/__init__.py
 [ping-scanner]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/ping_scanner.py
 [smb-finger]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/smbfinger.py
 [ssh-finger]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/sshfinger.py
 [tcp-scanner]: https://github.com/guardicore/monkey/blob/develop/monkey/infection_monkey/network/tcp_scanner.py
