# Firewall baseline with UFW

## Threat

Without a host firewall, every local service that binds `0.0.0.0` becomes Internet-reachable. Outbound-open hosts also make post-exploitation easy: malware can call home on any port.

## Do

Install and set default policies **before** enabling:

```bash
apt install -y ufw

ufw default deny incoming
ufw default deny outgoing
ufw default allow routed   # usually irrelevant on single-host VPS

# Always allow the SSH port you actually use — BEFORE enable
ufw limit 2222/tcp comment 'SSH rate-limited'

# Typical egress allowlist for a web app host
ufw allow out 53          # DNS (tcp/udp as needed; prefer systemd-resolved patterns)
ufw allow out 123/udp     # NTP
ufw allow out 80/tcp
ufw allow out 443/tcp
ufw allow out 587/tcp     # submission for msmtp (adjust to your provider)

ufw logging on
ufw --force enable
ufw status verbose
```

### Rate limiting

`ufw limit` uses iptables recent-match style limiting on new TCP connections. It will not stop a distributed slow scan, but it blunts simple floods against SSH.

### Application ports

Only open what the threat model listed:

```bash
ufw allow 443/tcp comment 'HTTPS'
# ufw allow 80/tcp comment 'HTTP redirector'   # only if needed
```

## Why

Default-deny egress is uncommon on desktop Linux and very useful on servers: unexpected outbound connections become loud failures instead of silent exfiltration. The cost is bookkeeping — every external dependency (package mirrors, APIs, SMTP) needs an explicit rule.

## Verify

```bash
ufw status numbered
# From outside: nmap or nc against closed ports should fail
# From the host:
curl -I https://deb.debian.org   # should work if 443/out allowed
```

Keep your SSH session. Open a second one after `ufw enable`.

## Rollback

```bash
ufw disable
# or
ufw reset
```

From console if locked out: disable UFW, fix rules, re-enable.

## Next

[intrusion-signals.md](intrusion-signals.md)
