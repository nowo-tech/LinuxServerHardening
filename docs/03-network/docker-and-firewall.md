# Docker and the host firewall

## Threat

Publishing a container port with Docker often bypasses UFW’s INPUT chain. Operators “close” a port in UFW and still expose it via `DOCKER` / `DOCKER-USER` forwarding. That gap is a classic production surprise.

## Do

### Prefer not to publish

- Bind services to `127.0.0.1` and put a host reverse proxy in front.
- Use user-defined bridges without `-p` when containers only talk to each other.

### If you must publish

1. Keep UFW rules honest for human expectation.
2. Add explicit allow/deny in the `DOCKER-USER` chain (evaluated before Docker’s accept rules).

IPv4 example (adjust interface and ports):

```bash
iptables -N DOCKER-USER 2>/dev/null || true
iptables -I DOCKER-USER -i eth0 -p tcp --dport 8080 -j DROP
iptables -I DOCKER-USER -i eth0 -s 203.0.113.0/24 -p tcp --dport 8080 -j ACCEPT
```

Persist rules with your distribution’s mechanism (`iptables-persistent` or a systemd unit). Repeat thoughtfully for **ip6tables** if you have IPv6.

### Do not

- Set `"iptables": false` in `daemon.json` unless you fully own container networking.
- Assume `ufw deny 8080` alone protects a published container.

## Why

Docker inserts its own NAT/filter rules. UFW manages a different path. Treat container publish as a **second firewall** you must configure explicitly.

## Verify

```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'
iptables -S DOCKER-USER
# External scan from another host against the published port
```

## Rollback

Flush custom `DOCKER-USER` rules you added, or restore from snapshot. Re-test published ports after every Docker upgrade.

## Next

[crowdsec.md](crowdsec.md)
