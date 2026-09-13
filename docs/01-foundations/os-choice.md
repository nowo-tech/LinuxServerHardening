# Choosing and preparing the OS

## Threat

An exotic, unmaintained, or desktop-oriented image increases patch lag and surprise services. Hardening cannot outrun an abandoned distribution.

## Do

Prefer a **stable server** image with long security support:

| Choice | When it fits |
|--------|----------------|
| Debian 12/13 | Default for this kit; predictable packaging |
| Ubuntu LTS | Fine if you already standardised on it — adapt package names |
| Rolling / testing | Labs only |

During install:

1. Enable OpenSSH server.
2. Set a strong root password for bootstrap only (lab) or use provider inject keys.
3. Prefer a static/reserved IP so inventory stays stable.
4. Take a snapshot named `pre-hardening` before automation.

Post-install minimum before hardening:

```bash
apt update && apt -y full-upgrade
reboot   # if a new kernel landed
hostnamectl
ip -br a
```

## Why

Security updates, AppArmor/SELinux defaults, and systemd behaviour differ by family. This kit’s examples and playbooks are validated on Debian; other distros need a porting pass.

## Verify

```bash
cat /etc/os-release
systemctl is-system-running
```

## Rollback

Rebuild from the provider image or restore the snapshot. Do not half-migrate a production hostname between major releases during a harden window.

## Next

[lab-setup.md](lab-setup.md)
