# Control coverage map

This kit aims for **practical completeness** of a Debian VPS baseline: identity, SSH, firewall/IDS, patching, mail alerts, malware/rootkit sensors, integrity, and audit. Use this map when reviewing gaps.

Legend: **A** = automated in Ansible (default or flag) · **D** = documented with Threat/Do/Why/Verify/Rollback · **O** = optional / advanced · **—** = intentionally omitted

| Control | Docs | Ansible | Notes |
|---------|------|---------|-------|
| Threat model & principles | D | — | Layer-0 reading |
| OS choice / lab prep | D | — | Debian-focused |
| Admin user + intent groups | D | A | `sshaccess` / `elevated` / `switchroot` |
| sudo / su limits | D | A | |
| SSH keys, port, AllowGroups | D | A | |
| SSH crypto (Kex/Ciphers/MACs) | D | A | |
| SSH moduli trim | D | A | |
| SSH MFA (TOTP) | D | O | `harden_enable_mfa_role` + enrol step |
| Password quality (pam_pwquality) | D | A | |
| NTP / timesync | D | A | Debian 13 timesyncd vs ≤12 ntp |
| Unattended security upgrades | D | A | |
| apticron + apt-listchanges | D | A | |
| Kernel sysctl hardening | D | A | |
| UFW default-deny in/out | D | A | |
| Fail2Ban sshd + mail actions | D | A | |
| PSAD + AUTO_IDS | D | A | |
| Dedicated iptables log + rotate | D | A | Feeds PSAD |
| IPv6 UFW log hooks | D | A | `before6.rules` |
| Docker vs UFW pitfalls | D | — | Doc only; environment-specific |
| CrowdSec alternative | D | — | Doc; choose one IPS |
| msmtp outbound alerts | D | A | Prefer over full MTA |
| ClamAV nightly | D | A | Flag |
| rkhunter | D | A | Flag |
| chkrootkit | D | O | Flag |
| AIDE integrity | D | O | Flag |
| auditd identity watches | D | A | Focused rules (expand carefully) |
| logwatch digests | D | O | Flag |
| Lynis audit + mail | D | A | |
| Listening sockets review (`ss`) | D | — | Ops checklist |
| hidepid / umask / lock root / GRUB | D | — | Advanced optional |
| Firejail | D | — | Advanced optional |
| deborphan review | D | — | Manual only |
| OSSEC/Wazuh | D | — | Pointed to as next step |
| Exim4 full MTA | — | — | Omitted; msmtp standard |
| Duress/panic passwords | — | — | Omitted on purpose |
| Legacy rng-tools tricks | — | — | Omitted on purpose |

## Residual risks (honest)

- Focused auditd rules are **not** a full enterprise syscall policy pack; enlarge only with disk/log budget.
- CrowdSec and Docker firewalling need human design — automation would be dangerously generic.
- Physical/console threats (GRUB, firmware) remain operator-owned.
- Application security (web apps, DB grants, secrets) is out of scope.

Update this table when you add a control.
