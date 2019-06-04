#!/usr/local/bin/python

import sys
import struct
import socket
import re
import operator
import netaddr
import itertools
import ipaddress
import exrex
import argparse
from re import sre_parse

parser = argparse.ArgumentParser("Convert a regular expression matching IP addressses to a list of CIDR blocks")
parser.add_argument('-l', '--list', action="store_true", dest="list_only", help="output list of IP addresses rather than a list of CIDR blocks")
args = parser.parse_args()

unichr = chr
# Change alpabeth used by exrex. We only need characters used in IPv4 and IPv6 addresses
exrex.CATEGORIES = {
        sre_parse.CATEGORY_SPACE: sorted(frozenset({})),
        sre_parse.CATEGORY_DIGIT: sorted(frozenset({'1', '6', '4', '5', '9', '2', '7', '0', '8', '3'})),
        'category_any': sorted(frozenset({'a','b','c','d','e','f', ':', '.', '1', '6', '4', '5', '9', '2', '7', '0', '8', '3'})),
        }

def ips(start, end, regex):
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    a = []
    for i in range(start, end):
        ip = socket.inet_ntoa(struct.pack('>I', i))
        if regex.match(ip):
            a.append(ip)
    return a

def gen_cidr(ip_start, ip_end):
    return netaddr.iprange_to_cidrs(ip_start, ip_end)

def create_range(ip_addresses):
    groups = []
    for _, g in itertools.groupby(enumerate(sorted(ip_addresses)), lambda ix:ix[0]-int(ix[1])):
        group = list(map(operator.itemgetter(1), g))
        if len(list(group)) > 1:
            groups.append("{}-{}".format(group[0], group[-1]))
        else:
            groups.append(str(group[0]))
    return groups

def is_valid(addr):
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

def sort_ip_list(ip_list):
    from IPy import IP
    ipl = [(IP(str(ip)).int(), ip) for ip in ip_list]
    ipl.sort()
    return [ip[1] for ip in ipl]

pattern = ''
for line in sys.stdin:
    if re.search(r"[*+]", line):
        print("Ignoring line '{}' because it contains unsupported quantifiers like + or *".format(line.rstrip()))
        continue
    pattern += line.strip(' \t\n') + "|"

pattern = str(pattern).rstrip('|')

a = set([])
try:
    #for i in list(exrex.generate(pattern, limit=sys.maxsize)):
    for i in list(exrex.generate(pattern, limit=(1<<32))):
        if not is_valid(i): continue
        a.add(ipaddress.ip_address(i))
except re.error:
    print("\nPattern error\n")
    exit(1)


if args.list_only:
    for i in sort_ip_list(list(a)):
        print(i)
else:
    for i in create_range(a):
        start = i.split('-')[0]
        end = i.split('-')[-1]
        for x in gen_cidr(start, end):
            print(str(x).replace('/32',''))
