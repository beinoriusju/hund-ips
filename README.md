# HUND IPS

This is a custom IPS solution for OpenWRT router to block malicious IP adresses as reported by Suricata IDS.

### How this works?

OpenWRT router mirrors traffic to Suricata IDS server that I'm running on separate computer (using Rasberi Pi4 with Debian). That same IDS computer is running Redis server. Suricata is configured to work with Redis. OpenWRT router listens for Redis que changes using Python and marks IP address banned if suricata alerts severity 1.

### Requires OpenWRT packages:

- python3
- python3-pip
- bash
- banip
- iptables-nft
- iptables-mod-tee

### Instruction:

1. Install Redis and Suriata on Rasberi Pi
2. Configure Suricata to use Redis
3. Copy contents of this Git repository to router `/root/ips`
4. Install all OpenWRT dependencies
5. Copy `/root/ips/init_d_script` to `/root/init.d/protect`
5. `service protect start` and `service protect enable`
6. `reboot`

### Why not use Suricata IPS?

Not sure how to plug it into OpenWRT...

### How can this be tested?

1. Observe OpenWRT `logread -f` for changes.
2. Create a custom Suricata rule that blocks IP address you know (I'm using mobile phone for this))
3. Visit `/etc/banip/banip.blocklist` should have 

### How to create a custom Suricata rule?

Read this: https://docs.suricata.io/en/latest/rule-management/adding-your-own-rules.html

Inspect Suricata configuration file `/etc/suricata/suricata.yaml` for **default-rule-path** entry. This is the place where you should place your custom rules file (eg. local.rules) Also add this file to rule-files as I did.

```
default-rule-path: /var/lib/suricata/rules

rule-files:
  - suricata.rules
  - local.rules
```


The contents of the `local.rules` file I'm using:

```
alert tcp <MY_MOBILE_IP> any -> any any (msg:"Testing blocking intruder"; priority:1; classtype:policy-violation; sid:1; rev:2;)
```

Restart Suricata `service suricata restart`

If successful single visit from mobile to your netowk should result in mobile phone IP ban. IP addresses are appended to `/etc/banip/banip.blocklist`