# Kernel and sysctl hardening

## Threat

Default kernel networking knobs favour compatibility. On a public server, that often means accepting spoofed packets, following shady redirects, or exposing more of `/proc` than operators need.

## Do

Create a dedicated sysctl drop-in:

```bash
# /etc/sysctl.d/60-nowo-hardening.conf
# Ignore ICMP redirects (common MITM helper)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Do not send redirects either
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Reverse-path filtering (strict where possible)
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# SYN cookies against simple SYN floods
net.ipv4.tcp_syncookies = 1

# Ignore source-routed packets
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Log martians
net.ipv4.conf.all.log_martians = 1

# ASLR
kernel.randomize_va_space = 2
```

Apply:

```bash
sysctl --system
```

### `/proc` hidepid (optional)

Mount options can hide other users’ processes from unprivileged accounts. Test with your monitoring agent first — some scrapers expect broad `/proc` visibility.

## Why

These settings are cheap, reversible, and close well-known networking foot-guns. They do not replace application security; they shrink the kernel-facing attack surface.

## Verify

```bash
sysctl net.ipv4.tcp_syncookies net.ipv4.conf.all.rp_filter kernel.randomize_va_space
```

## Rollback

```bash
rm /etc/sysctl.d/60-nowo-hardening.conf
sysctl --system
```

## Next

[../05-detection/auditing.md](../05-detection/auditing.md)
