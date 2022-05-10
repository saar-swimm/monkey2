---
title: "Network Segmentation"
date: 2020-08-12T13:05:05+03:00
draft: false
description: "Verify your network is properly segmented."
weight: 4
---

## Overview

Segmentation is a method of creating secure zones in data centers and cloud deployments. It allows organizations to isolate workloads from one another and secure them individually, typically using policies. A useful way to test your company's segmentation effectiveness is to ensure that your network segments are properly separated (e.g., your development environment is isolated from your production environment and your applications are isolated from one another).

[Segmentation is key](https://www.guardicore.com/use-cases/micro-segmentation/) to protecting your network. It can reduce the network's attack surface and minimize the damage caused during a breach.

You can use the Infection Monkey's cross-segment traffic feature to verify that your network segmentation configuration is adequate. This way, you can ensure that, even if a bad actor breaches your defenses, they can't move laterally between segments.


## Configuration

- **Network -> Network analysis -> Network segmentation testing** This configuration setting allows you to define
 subnets that should be segregated from each other. If any of the provided networks can reach each other, you'll see it
 in the security report.
- **(Optional) Network -> Scope** You can disable **Local network scan** and leave all other options at the default setting if you only want to test for network segmentation without any lateral movement.
- **(Optional) Monkey -> Post-Breach Actions** If you only want to test segmentation in the network, you can turn off all post-breach actions. These actions simulate an attacker's behavior after getting access to a new system, so they might trigger your defense solutions and interrupt the segmentation test.

## Suggested run mode

Execute The Infection Monkey on machines in different subnetworks using the “Manual” run option.

 Note that if the Infection Monkey can't communicate to the Monkey Island, it will
 not be able to send scan results, so make sure all machines can reach the the Monkey Island.

![How to configure network segmentation testing](/images/usage/scenarios/segmentation-config.png "How to configure network segmentation testing")


## Assessing results

Check the infection map and security report for segmentation problems. Ideally, all scanned nodes should only have edges with the Monkey Island Server.

![Map](/images/usage/use-cases/segmentation-map.PNG "Map")
