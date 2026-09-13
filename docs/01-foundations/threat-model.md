# Threat model (practical)

## Threat

A public IPv4 address attracts scanners within minutes. Typical early noise:

- SSH password guessing on port 22
- Probes for exposed admin panels
- Exploitation of unpatched services you forgot were listening

Without a model, you harden the wrong layer (for example fancy banners) while leaving password root login open.

## Do

Fill this table for your host:

| Question | Example answer |
|----------|----------------|
| Who are the admins? | Alice and Bob |
| From where do they connect? | Home + travel networks (unknown IPs) |
| What must stay reachable from the Internet? | HTTPS :443, SSH :2222 |
| What data is on disk? | App DB dump nightly; `.env` with API keys |
| What is unacceptable? | Silent rootkit; ransomware; data exfil |
| What is acceptable residual risk? | Brief downtime for emergency reboot |

### Worked example: single-app VPS

```text
Attacker goal A: steal database dumps
  Mitigations: disk permissions, no password SSH, egress deny by default,
               alerts on new listeners, daily integrity scan

Attacker goal B: use the VPS in a botnet
  Mitigations: unattended security updates, fail2ban/psad signals,
               no unused packages, outbound deny except allowlist

Attacker goal C: lock you out for ransom
  Mitigations: offsite backups (out of scope here), console access,
               second admin key stored offline
```

## Why

Threat modeling focuses effort. A home lab behind NAT with no port forwards needs less inbound firewall drama than a dual-stack VPS with a public A record. Same tools, different priority.

## Verify

After you finish the guide, map each control back to a row in your table. Orphan controls (no mapped threat) are candidates for removal or documentation as “compliance only.”

## Rollback

Models change. When you expose a new port for an app, update the table **before** opening the firewall rule.

## Next

[lab-setup.md](lab-setup.md)
