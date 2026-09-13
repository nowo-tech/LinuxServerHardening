# Control coverage map

This kit aims for **practical completeness** of a Debian VPS baseline: identity, SSH, firewall/IDS, patching, mail alerts, malware/rootkit sensors, integrity, and audit.

Legend: **A** = automated (on by default) · **F** = automated behind a flag (off by default) · **D** = documented · **—** = intentionally omitted

| Control | Docs | Ansible | Notes |
|---------|------|---------|-------|
| Threat model & principles | D | — | Layer-0 reading |
| OS choice / lab prep | D | — | Debian 12/13 asserted |
| Admin user + intent groups | D | A | Password set `on_create` only |
| sudo / su limits | D | A | Passwordless sudo **off** by default |
| SSH keys, port, AllowGroups | D | A | Separate bootstrap vs runtime inventories |
| SSH crypto (Kex/Ciphers/MACs) | D | A | |
| SSH moduli trim | D | A | |
| SSH MFA (TOTP) | D | F | `harden_enable_mfa_role` + enrol + disable nullok |
| Password quality (pam_pwquality) | D | A | Writes `/etc/security/pwquality.conf` |
| NTP / timesync | D | A | Debian 13 timesyncd vs ≤12 ntp |
| Unattended security upgrades | D | A | Auto-reboot **off** by default |
| apticron + apt-listchanges | D | A | |
| Kernel sysctl hardening | D | A | |
| UFW default-deny in/out | D | A | |
| Fail2Ban sshd + mail actions | D | A | |
| PSAD (detect / alert) | D | A | |
| PSAD AUTO_IDS (auto-block) | D | F | `harden_psad_auto_ids` — opt-in |
| Dedicated iptables log + rotate | D | A | Rate-limited LOG rules |
| IPv6 UFW log hooks | D | A | `before6.rules` |
| Docker vs UFW pitfalls | D | — | Doc only |
| CrowdSec alternative | D | — | Doc; choose one IPS |
| msmtp outbound alerts | D | A | `0600` msmtprc; test mail surfaced |
| ClamAV scoped nightly | D | F | Paths under `harden_clamav_scan_paths` |
| rkhunter | D | A | |
| chkrootkit | D | F | |
| AIDE integrity | D | F | Debian `aide.db.new` → `aide.db` |
| auditd identity watches | D | A | Focused rules |
| logwatch digests | D | A | |
| Lynis on harden apply | D | — | Off by default (`harden_lynis_force_run`) |
| Lynis via `03-audit.yml` | D | A | Forces a run; Debian packages only by default |
| Third-party Lynis APT repo | D | F | `harden_allow_third_party_lynis_repo` — supply-chain opt-in |
| Listening sockets review (`ss`) | D | — | Ops checklist |
| hidepid / umask / lock root / GRUB | D | — | Advanced optional |
| Firejail / deborphan / OSSEC | D | — | Advanced optional |
| Exim4 / duress passwords / rng-tools | — | — | Omitted on purpose |

## Safer defaults (lab overrides)

| Variable | Production default | Common lab override |
|----------|--------------------|---------------------|
| `harden_passwordless_sudo` | `false` | `true` |
| `harden_auto_reboot` | `false` | `true` |
| `harden_psad_auto_ids` | `false` | `true` (careful) |
| `harden_enable_clamav` / `aide` / `chkrootkit` | `false` | `true` as needed |

## Residual risks

- Focused auditd rules are not a full enterprise syscall pack.
- CrowdSec and Docker firewalling need human design.
- Physical/console threats remain operator-owned.
- Application security is out of scope.
