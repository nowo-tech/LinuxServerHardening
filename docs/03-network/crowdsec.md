# CrowdSec as an alternative IPS

## Threat

Fail2Ban is excellent at “same IP keeps failing sshd,” but modern scrapers rotate IPs and share patterns across fleets. A collaborative engine can catch campaigns a single host never sees twice.

## Do

Install only **one** primary application IPS at first (Fail2Ban **or** CrowdSec). Dual stacks double the ban logic and the lockout risk.

```bash
# Follow current upstream install for Debian, then:
apt install -y crowdsec crowdsec-firewall-bouncer-iptables
# Prefer nftables bouncer if your firewall path is nft-native

cscli collections list
cscli metrics
```

Unban when you trap yourself:

```bash
cscli decisions delete --ip A.B.C.D
```

Wire notifications once mail works. Keep SSH console access during the first week.

## Why

| Tool | Best at |
|------|---------|
| Fail2Ban | Local log signatures, simple jails, tiny footprint |
| CrowdSec | Shared signals, richer parsers, modern scrapers |
| PSAD | Packet/scan patterns from firewall logs |

They complement at different layers; they fight if two tools ban/unban the same IP differently.

## Verify

```bash
cscli metrics
cscli decisions list
```

## Rollback

```bash
systemctl disable --now crowdsec crowdsec-firewall-bouncer
# Re-enable Fail2Ban jails if you had disabled them
```

## Next

[../04-host-baseline/time-sync.md](../04-host-baseline/time-sync.md)
