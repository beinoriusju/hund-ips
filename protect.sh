#!/bin/bash

SCRIPT_DIR=$(dirname "$0")
SURICATA_IP="192.168.1.50"

echo "Starting IPS in 30 seconds..."

sleep 30

echo "Starting IPS"

iptables -A POSTROUTING -t mangle -o br-lan ! -s $SURICATA_IP -j TEE --gateway $SURICATA_IP
iptables -A PREROUTING -t mangle -i br-lan ! -d $SURICATA_IP -j TEE --gateway $SURICATA_IP

python -u "$SCRIPT_DIR/ips.py"