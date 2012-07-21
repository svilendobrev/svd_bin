#!/bin/sh
sudo /sbin/sysctl -w net.ipv4.ip_forward=1
sudo /sbin/ifconfig eth0:1 192.168.20.1 netmask 255.255.255.0
sudo /sbin/iptables -t nat -I POSTROUTING -s 192.168.20.0/24 -j MASQUERADE
#/sbin/service smb  restart

# client:
# 192.168.20.2 netmask 255.255.255.0
# 192.168.20.... netmask 255.255.255.0
# gateway 192.168.20.1
# dns, kato na BTK, cat /etc/resolv.conf	192.168.1.1
