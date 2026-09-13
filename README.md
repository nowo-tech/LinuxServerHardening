# Linux Server Hardening

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/nowo-tech/LinuxServerHardening/actions/workflows/ci.yml/badge.svg)](https://github.com/nowo-tech/LinuxServerHardening/actions/workflows/ci.yml)
[![Ansible](https://img.shields.io/badge/Ansible-2.14%2B-red?logo=ansible)](https://docs.ansible.com/)
[![Debian](https://img.shields.io/badge/Debian-12%20%7C%2013-A81D33?logo=debian)](https://www.debian.org/)

**Linux Server Hardening** is a Nowo Tech learning kit: a layered security guide plus Ansible automation you can run on a fresh Debian host.

It is written for people who want to **understand each control**, not only apply a checklist. Every chapter follows the same pattern:

1. **Threat** — what goes wrong if you skip this
2. **Do** — concrete commands or playbook tags
3. **Why** — the reasoning in plain language
4. **Verify** — how to prove the control works
5. **Rollback** — how to undo it safely

## Who this is for

- Operators bringing up VPS or bare-metal Debian servers
- Developers who own a small production box end-to-end
- Teams that want a repeatable baseline before app deploy

It is **not** a compliance product, a CIS auditor replacement, or a substitute for your organisation’s security policy.

## Mental model: six defense layers

```text
┌─────────────────────────────────────────────────────────┐
│ 6. Operations      monitoring, mail alerts, re-audit    │
├─────────────────────────────────────────────────────────┤
│ 5. Detection       auditd, scanners, integrity checks   │
├─────────────────────────────────────────────────────────┤
│ 4. Host baseline   packages, passwords, auto-updates    │
├─────────────────────────────────────────────────────────┤
│ 3. Network edge    firewall, rate limits, IDS hooks     │
├─────────────────────────────────────────────────────────┤
│ 2. Access control  SSH keys, groups, sudo/su policy     │
├─────────────────────────────────────────────────────────┤
│ 1. Foundations     threat model, OS choice, lab safety  │
└─────────────────────────────────────────────────────────┘
```

Work bottom-up. Changing SSH before you have a firewall recovery path is a common lock-out pattern; the guide orders steps to reduce that risk.

## Repository layout

```text
docs/                 Didactic guide (read in order)
ansible/              Automation that mirrors the layers
  playbooks/          Entry points (bootstrap → harden → audit)
  roles/              One concern per role
  inventories/lab/    Example inventory (replace with yours)
  group_vars/         Non-secret defaults + vault placeholders
```

| Path | Purpose |
|------|---------|
| [docs/00-start-here.md](docs/00-start-here.md) | How to use the kit safely |
| [docs/01-foundations/](docs/01-foundations/) | Threat model, OS choice, lab safety |
| [docs/02-access-control/](docs/02-access-control/) | Users, SSH (incl. crypto + MFA), privilege boundaries |
| [docs/03-network/](docs/03-network/) | Firewall, IDS, Docker caveats, CrowdSec |
| [docs/04-host-baseline/](docs/04-host-baseline/) | NTP, updates, passwords, kernel knobs |
| [docs/05-detection/](docs/05-detection/) | auditd, AIDE, malware/rootkit checks |
| [docs/06-operations/](docs/06-operations/) | Mail, logwatch, day-2 review |
| [docs/07-advanced/](docs/07-advanced/) | GRUB, umask, hidepid, Firejail, and more |
| [docs/CONTROL-COVERAGE.md](docs/CONTROL-COVERAGE.md) | What is documented vs automated |
| [ansible/README.md](ansible/README.md) | How to run the playbooks |

## Quick start (automation)

> **Warning:** These playbooks change SSH, firewall, and privilege settings. Use a disposable lab VM first. Keep a console/VNC session open until you confirm key-based login on the new port.

```bash
git clone https://github.com/nowo-tech/LinuxServerHardening.git
cd LinuxServerHardening/ansible

# 1) Inventories: bootstrap (root) vs runtime (admin + new SSH port)
cp inventories/lab/hosts.bootstrap.yml.example inventories/lab/hosts.bootstrap.yml
cp inventories/lab/hosts.yml.example inventories/lab/hosts.yml
# Edit both: set ansible_host; align ansible_user/port in hosts.yml with vars

# 2) Variables + Vault secrets
cp group_vars/all/vars.yml.example group_vars/all/vars.yml
cp group_vars/all/vault.yml.example group_vars/all/vault.yml
# Lab tip: set harden_passwordless_sudo: true so become is easier
ansible-vault encrypt group_vars/all/vault.yml

# 3) Bootstrap admin user + SSH key (as root once)
ansible-playbook -i inventories/lab/hosts.bootstrap.yml playbooks/01-bootstrap.yml \
  --ask-vault-pass --ask-pass

# 4) Harden as the new admin user (runtime inventory)
ansible-playbook -i inventories/lab/hosts.yml playbooks/02-harden.yml \
  --ask-vault-pass --ask-become-pass --key-file ~/.ssh/lab_ed25519
```

Re-runs (runtime inventory already sets `ansible_port`):

```bash
ansible-playbook -i inventories/lab/hosts.yml playbooks/02-harden.yml \
  --ask-vault-pass --ask-become-pass --key-file ~/.ssh/lab_ed25519
```

## Quick start (manual learning path)

If you prefer to learn by hand before automating:

1. Read [docs/00-start-here.md](docs/00-start-here.md)
2. Complete [docs/01-foundations/](docs/01-foundations/)
3. Follow layers 2 → 6 in order
4. Use the playbooks as a regression suite for the same controls

## Design choices (and why)

| Choice | Reason |
|--------|--------|
| Debian-focused examples | Validated on Debian 12/13 (asserted in plays) |
| Ansible Vault for secrets | Passwords and SMTP tokens must not live in git history |
| Safer production defaults | No NOPASSWD, no auto-reboot, no PSAD auto-block unless opted in |
| Default-deny firewall (in and out) | Limits both inbound scanners and unexpected C2 egress |
| Key-only SSH, no root login | Removes the highest-value, most-probed credentials |
| Security-only unattended upgrades | Patches critical CVEs without surprise feature bumps |
| Separate bootstrap vs runtime inventories | Avoids `ansible_user: root` sticking on harden plays |

## Safety contract

- Read each role before enabling it on a machine that matters.
- Automation is a **starting baseline**, not a finished security program.
- You own verification: open a second session, test login, test firewall, test mail.
- Production needs backups, monitoring, and an incident plan beyond this kit.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep documentation didactic: every new control needs Threat / Do / Why / Verify / Rollback.

## License

MIT — see [LICENSE](LICENSE).
