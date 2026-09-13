# Advanced host controls

Optional controls with higher operational cost. Enable after the core layers are stable.

## Lock the root password database entry

### Threat

`PermitRootLogin no` stops network root SSH. A guessable root password still matters at the console and for some recovery paths.

### Do

```bash
# Only after sudo for admin works and a console is available
passwd -l root
passwd -S root   # should show L
```

### Why / risk

`sulogin` during emergency boot may expect an unlocked root. Know your provider’s rescue story before locking.

---

## Default umask

### Threat

World-readable home files and shared dirs leak secrets created by careless apps.

### Do

```bash
# /etc/login.defs
UMASK 027

# /etc/profile and /etc/bash.bashrc for interactive shells
umask 027

# /root/.bashrc
umask 077
```

### Risk

Services that expect world-readable files under `/etc` can break. Test after change.

---

## Hide other users’ processes (`hidepid`)

### Threat

Unprivileged local users inspect process command lines (tokens in argv, etc.).

### Do

```fstab
proc /proc proc defaults,hidepid=2 0 0
```

```bash
mount -o remount,hidepid=2 /proc
```

### Risk

Monitoring agents and some desktop tools misbehave. Flag as optional in automation.

---

## Password-protect GRUB

### Threat

Physical or console attackers edit kernel cmdline (`init=/bin/sh`) and reset passwords.

### Do

```bash
grub-mkpasswd-pbkdf2 -c 100000
# Create /etc/grub.d/01_password with superusers + password_pbkdf2 ...
# Keep the default menu entry unrestricted for unattended reboot
update-grub
```

Protects GRUB only — firmware/BIOS passwords are separate.

---

## Application sandboxing with Firejail

Useful on admin workstations or servers that run browsers/mail clients. Less common on headless API boxes.

```bash
apt install -y firejail firejail-profiles
# Optional: wrap binaries via /usr/local/bin symlinks to firejail
firejail --list
```

---

## Remove orphaned packages carefully

```bash
apt install -y deborphan
deborphan                 # review by hand
# apt --autoremove purge $(deborphan)   # never blind in production
```

Orphan ≠ unused dependency of something you still need.

---

## Host IDS beyond auditd (OSSEC / Wazuh)

Compile-or-agent HIDS is valuable at fleet scale. For a single VPS, prefer auditd + AIDE + Lynis first; graduate to Wazuh/OSSEC when you need central correlation.

---

## Intentionally out of scope

| Idea | Reason |
|------|--------|
| Duress / “panic” passwords that wipe the box | Extreme physical-coercion niche; high accidental-destruction risk |
| Forcing `rng-tools` onto `/dev/urandom` | Obsolete guidance on modern kernels |
| Full Exim4 smarthost stacks | Larger attack surface; kit standardises on msmtp |

## Next

[../CONTROL-COVERAGE.md](../CONTROL-COVERAGE.md)
