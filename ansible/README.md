# Ansible automation

Playbooks mirror the documentation layers. Read [../docs/00-start-here.md](../docs/00-start-here.md) before the first run. See [../docs/CONTROL-COVERAGE.md](../docs/CONTROL-COVERAGE.md) for what each flag enables.

## Requirements

- Control node: Ansible 2.14+ (collections `ansible.builtin`, `ansible.posix`, `community.general`)
- Target: Debian 12 or 13 with Python 3
- Network path from control node to target on SSH

```bash
ansible-galaxy collection install -r requirements.yml
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

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/02-harden.yml \
  --ask-vault-pass --tags firewall,ssh,ntp
```

Tags include: `packages`, `ntp`, `sysctl`, `ssh`, `mfa`, `passwords`, `updates`, `firewall`, `ids`, `mail`, `malware`, `integrity`, `chkrootkit`, `aide`, `auditd`, `logwatch`, `lynis`.

## Feature flags (`vars.yml`)

| Variable | Default | Effect |
|----------|---------|--------|
| `harden_enable_mfa_role` | `false` | Install TOTP PAM wiring |
| `harden_ssh_mfa_enable` | `false` | Enforce `publickey,keyboard-interactive` |
| `harden_enable_aide` | `true` | AIDE init + daily cron |
| `harden_enable_logwatch` | `true` | Daily HTML mail digest |
| `harden_enable_chkrootkit` | `true` | chkrootkit package + daily |
| `harden_auto_reboot` | `true` | Unattended reboot after security updates |

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
  time_sync/          systemd-timesyncd or ntp
  host_sysctl/        network/kernel sysctl drop-in
  ssh_hardening/      sshd drop-in + moduli + crypto
  ssh_mfa/            optional TOTP PAM
  password_policy/    pam_pwquality
  auto_updates/       unattended-upgrades + apticron
  firewall_stack/     ufw + fail2ban + psad + iptables log
  outbound_mail/      msmtp
  malware_scan/       clamav
  integrity_checks/   rkhunter
  rootkit_extra/      chkrootkit
  file_integrity/     AIDE
  audit_framework/    auditd rules
  log_digest/         logwatch
  security_audit/     lynis
```
