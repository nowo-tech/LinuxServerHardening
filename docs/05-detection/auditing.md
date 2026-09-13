# Auditing with auditd

## Threat

Without syscall auditing, “who changed `/etc/passwd` at 02:14?” becomes guesswork after an incident. Journals help, but audit rules capture kernel-level events security teams expect.

## Do

```bash
apt install -y auditd audispd-plugins
systemctl enable --now auditd
```

Start with a **small** local ruleset you understand. Example `/etc/audit/rules.d/20-identity.rules`:

```text
# Watch identity and trust files
-w /etc/passwd -p wa -k identity
-w /etc/group  -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/sudoers -p wa -k privilege
-w /etc/sudoers.d -p wa -k privilege
-w /etc/ssh/sshd_config -p wa -k sshd
-w /etc/ssh/sshd_config.d -p wa -k sshd
```

Load:

```bash
augenrules --load
auditctl -l
```

Search:

```bash
ausearch -k identity -ts recent
```

Community “full coverage” rule packs exist; import them only after you have log shipping and disk budget. A huge ruleset on a tiny VPS can crush I/O.

## Why

Targeted watches on identity and privilege files catch many real intrusions (user add, sudoers tweak, sshd drop-in) with little noise. Broad exec auditing is powerful and expensive — graduate to it later.

## Verify

```bash
# As admin with sudo:
sudo touch /etc/passwd
sudo ausearch -k identity -ts recent | tail
```

## Rollback

```bash
rm /etc/audit/rules.d/20-identity.rules
augenrules --load
```

## Next

[scanners.md](scanners.md)
