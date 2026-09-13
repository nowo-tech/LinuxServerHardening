# Time synchronisation (NTP)

## Threat

TLS, TOTP MFA, log correlation, and certificate validation all assume clocks are roughly correct. A drifting clock breaks MFA, confuses incident timelines, and can cause “mysterious” auth failures.

## Do

### Debian 13+ (systemd-timesyncd)

```bash
timedatectl set-ntp true
mkdir -p /etc/systemd/timesyncd.conf.d
cat >/etc/systemd/timesyncd.conf.d/nowo.conf <<'EOF'
[Time]
NTP=pool.ntp.org
FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org
EOF
systemctl restart systemd-timesyncd
timedatectl status
timedatectl timesync-status
```

### Debian 12 and older (ntp package)

```bash
apt install -y ntp
# Ensure a pool line exists:
# pool pool.ntp.org iburst
systemctl restart ntp
ntpq -p
```

Firewall: allow outbound UDP/123 (already in the kit’s default egress allowlist).

## Why

Public NTP pools are fine for most VPS hosts. High-assurance environments should pin to organisational NTP and monitor offset. Wrong timezone is annoying; wrong **UTC offset drift** is a security bug.

## Verify

```bash
date -u
timedatectl show-timesync 2>/dev/null || ntpq -p
```

## Rollback

```bash
timedatectl set-ntp false
# or purge ntp / remove the drop-in
```

## Next

[updates-and-passwords.md](updates-and-passwords.md)
