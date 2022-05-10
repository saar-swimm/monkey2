---
title: "Other"
date: 2020-08-12T13:07:55+03:00
draft: false
description: "Tips and tricks about configuring Monkeys for your needs."
weight: 100
---

## Overview
This page provides additional information about configuring the Infection Monkey, tips and tricks and creative usage scenarios.

## Custom behaviour

If you want the Infection Monkey to run a specific script or tool after it breaches a machine, you can configure it in
**Configuration -> Monkey -> Post-breach**. Input commands you want to execute in the corresponding fields.
You can also upload files and call them through the commands you entered.

## Accelerate the test

To improve scanning speed you could **specify a subnet instead of scanning all of the local network**.

The following configuration values also have an impact on scanning speed:
- **Credentials** - The more usernames and passwords you input, the longer it will take the Infection Monkey to scan machines that have
remote access services. The Infection Monkey agents try to stay elusive and leave a low impact, and thus brute-forcing takes longer than with loud conventional tools.
- **Network scope** - Scanning large networks with a lot of propagations can become unwieldy. Instead, try to scan your
networks bit by bit with multiple runs.
- **Post-breach actions** - If you only care about propagation, you can disable most of these.
- **Internal -> TCP scanner** - Here you can trim down the list of ports the Infection Monkey tries to scan, improving performance.

## Combining different scenarios

The Infection Monkey is not limited to the scenarios mentioned in this section. Once you get the hang of configuring it, you might come up with your own use case or test all of the suggested scenarios at the same time! Whatever you do, the Infection Monkey's Security, ATT&CK and Zero Trust reports will be waiting for you with your results!

## Persistent scanning

Use **Monkey -> Persistent** scanning configuration section to either run periodic scans or increase the reliability of exploitations by running consecutive scans with the Infection Monkey.

## Credentials

Every network has its old "skeleton keys" that it should have long discarded. Configuring the Infection Monkey with old and stale passwords will enable you to ensure they were really discarded.

To add the old passwords, go to the Monkey Island's **Exploit password list** under **Basic - Credentials** and use the "+" button to add the old passwords to the configuration. For example, here we added a few extra passwords (and a username as well) to the configuration:

![Exploit password and user lists](/images/usage/scenarios/user-password-lists.png "Exploit password and user lists")

## Check logged and monitored terminals

To see the Infection Monkey executing in real-time on your servers, add the **post-breach action** command:
`wall “Infection Monkey was here”`. This post-breach command will broadcast a message across all open terminals on the servers the Infection Monkey breached to achieve the following:
- Let you know the Monkey ran successfully on the server.
- Let you follow the breach “live” alongside the infection map.
- Check which terminals are logged and monitored inside your network.

![How to configure post breach commands](/images/usage/scenarios/pba-example.png "How to configure post breach commands.")
