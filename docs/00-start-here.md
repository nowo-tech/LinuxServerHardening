# Start here

This kit teaches **why** Linux server controls exist, then helps you apply them by hand or with Ansible.

## Before you touch a production host

1. **Snapshot or clone a lab VM.** Prefer a throwaway VPS or local QEMU/VirtualBox image.
2. **Open a provider console** (serial, VNC, or cloud “recovery”). If SSH breaks, you still have a way in.
3. **Write down recovery facts:** current SSH port, root password (lab only), admin username, public key path.
4. **Decide your threat model** using [01-foundations/threat-model.md](01-foundations/threat-model.md).

## How each chapter is structured

| Section | Question it answers |
|---------|---------------------|
| Threat | What fails if we skip this? |
| Do | What exact steps do I take? |
| Why | Why this setting and not another? |
| Verify | How do I prove it worked? |
| Rollback | How do I undo without rebuilding? |

Copy that pattern when you add controls of your own.

## Suggested order

```text
Foundations → Access → Network → Host baseline → Detection → Operations
```

Skipping ahead is fine for experienced operators, but **never** change the SSH port until:

- your admin user exists,
- your public key works,
- the firewall already allows the **new** port,
- a console session is open.

## Lab vs production

| Topic | Lab | Production |
|-------|-----|------------|
| Secrets in Vault | Optional (still good practice) | Mandatory |
| Default-deny egress | Recommended | Required if you can list needed ports |
| Mail alerts | Use a throwaway inbox | Use a monitored inbox / ticket route |
| Scanners (ClamAV, rkhunter) | Nightly is fine | Schedule by load; tune false positives |
| Reboots after security updates | Automatic OK | Windowed / approved |

## What “good enough” looks like after day one

- Root cannot SSH in
- Password SSH is off; keys only
- Only members of an SSH allow-group can connect
- Firewall denies unexpected inbound traffic
- Security updates install without waiting for you
- You receive at least one test alert email

Then iterate: detection depth, kernel hardening, application jails, and continuous audit.

## Next

Continue with [01-foundations/principles.md](01-foundations/principles.md).
