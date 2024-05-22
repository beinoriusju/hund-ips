# HUND IPS

This is a custom IPS solution for OpenWRT router to block malicious IP adresses as reported by Redis server (running outside Router).

### How this works?

OpenWRT router listens for Redis que using Python and marks coming IP address banned by appending banip blocklist file `/etc/banip/banip.blocklist`

### Requires OpenWRT packages:

- python3
- python3-pip
- bash
- banip

### Instruction:

1.  Install all OpenWRT dependencies
2. Copy contents of this Git repository to router `/root/ips`
3. Copy `/root/ips/init_d_script` to `/root/init.d/protect`
5. `service protect start` and `service protect enable`
6. `reboot`

### How can this be tested/debugged?

1. Observe OpenWRT `logread -f` for changes.
2. Add IP to Redis list `router-block`
3. `cat /etc/banip/banip.blocklist` should have that IP after a few seconds