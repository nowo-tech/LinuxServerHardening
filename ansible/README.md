# Ansible automation

Playbooks mirror the documentation layers. Read [../docs/00-start-here.md](../docs/00-start-here.md) before the first run.

## Requirements

- Control node: Ansible 2.14+ (collections `ansible.builtin`, `ansible.posix`, `community.general`)
- Target: Debian 12 or 13 with Python 3
- Network path from control node to target on SSH

```bash
ansible-galaxy collection install ansible.posix community.general
```

## Configure

```bash
cd ansible
cp inventories/lab/hosts.yml.example inventories/lab/hosts.yml
cp group_vars/all/vars.yml.example group_vars/all/vars.yml
cp group_vars/all/vault.yml.example group_vars/all/vault.yml

# Edit hosts.yml, vars.yml, then encrypt secrets:
ansible-vault encrypt group_vars/all/vault.yml
```

## Plays

| Playbook | Runs as | Purpose |
|----------|---------|---------|
| `playbooks/01-bootstrap.yml` | `root` | Admin user, groups, SSH key, sudo |
| `playbooks/02-harden.yml` | admin user | Full baseline (SSH, firewall, detection…) |
| `playbooks/03-audit.yml` | admin user | Lynis run + optional mail report |

## Tags

On `02-harden.yml` you can limit scope:

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/02-harden.yml \
  --ask-vault-pass --tags firewall,ssh
```

Available tags: `packages`, `ssh`, `passwords`, `updates`, `sysctl`, `firewall`, `ids`, `mail`, `malware`, `integrity`, `auditd`, `lynis`.

## Safety

1. Snapshot the VM.
2. Keep provider console open.
3. Run bootstrap, then verify key login.
4. Run harden with `--check` first if you want a dry run (some tasks are not fully check-mode safe).

## Directory map

```text
roles/
  bootstrap/          packages needed early
  admin_user/         groups + user + key + sudo/su
  host_sysctl/        network/kernel sysctl drop-in
  ssh_hardening/      sshd drop-in + moduli
  password_policy/    pam_pwquality
  auto_updates/       unattended-upgrades
  firewall_stack/     ufw + fail2ban + psad
  outbound_mail/      msmtp
  malware_scan/       clamav
  integrity_checks/   rkhunter
  audit_framework/    auditd rules
  security_audit/     lynis
```
