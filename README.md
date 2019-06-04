# Rex2cidr

Tool to convert simple regular expressions matching IPv4 addresses to a list of CIDR blocks.

## Prerequisites

Docker installed on your host.

## Usage

Generate list of CIDR blocks from regular expression:

        $ echo -n "^1\.1\.1\.([0-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-5]))$" | ./run_docker.sh

        1.1.1.0/24

Generate list of matching IP addresses (do not combine them to CIDR blocks)

        $ echo -n "^10\.0\.0\.([1-9]|1[0-5])$" | ./run_docker.sh -l
        
        10.0.0.1
        10.0.0.2
        10.0.0.3
        10.0.0.4
        10.0.0.5
        10.0.0.6
        10.0.0.7
        10.0.0.8
        10.0.0.9
        10.0.0.10
        10.0.0.11
        10.0.0.12
        10.0.0.13
        10.0.0.14
        10.0.0.15

Generate list of CIDR blocks from multiple regular expressions. Separate them with newlines or use regex alternations:

        $ echo -n "^1\.1\.1\.([0-9]|[1-9][0-9]|1([0-9][0-9])|2([0-4][0-9]|5[0-5]))$
          ^192\.168\.0\.([1-9]|[1-2][0-9]|3[0-2])$" | ./run_docker.sh

        1.1.1.0/24
        192.168.0.1
        192.168.0.2/31
        192.168.0.4/30
        192.168.0.8/29
        192.168.0.16/28
        192.168.0.32



## Limitations

The tool is primarily intended to convert regular expressions generated from IP regular expression builders which exactly match an IP address.

The tool is sound but it will not complete in reasonable time if you try to convert regular expressions like `^10.*` matching a large number or even infinite many strings.
