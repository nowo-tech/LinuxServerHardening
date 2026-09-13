# Documentation index

Read in order for the full learning path.

1. [00 — Start here](00-start-here.md)
2. Foundations
   - [Principles](01-foundations/principles.md)
   - [Threat model](01-foundations/threat-model.md)
   - [OS choice](01-foundations/os-choice.md)
   - [Lab setup](01-foundations/lab-setup.md)
3. Access control
   - [Admin identity](02-access-control/admin-identity.md)
   - [SSH service](02-access-control/ssh-service.md)
   - [SSH MFA](02-access-control/ssh-mfa.md)
4. Network
   - [Firewall](03-network/firewall.md)
   - [Intrusion signals](03-network/intrusion-signals.md)
   - [Docker and firewall](03-network/docker-and-firewall.md)
   - [CrowdSec](03-network/crowdsec.md)
5. Host baseline
   - [Time sync](04-host-baseline/time-sync.md)
   - [Updates and passwords](04-host-baseline/updates-and-passwords.md)
   - [Kernel and sysctl](04-host-baseline/kernel-and-sysctl.md)
6. Detection
   - [Auditing](05-detection/auditing.md)
   - [AIDE](05-detection/file-integrity-aide.md)
   - [Scanners](05-detection/scanners.md)
7. Operations
   - [Mail alerts](06-operations/mail-alerts.md)
   - [Log digests](06-operations/log-digests.md)
   - [Continuous review](06-operations/continuous-review.md)
8. Advanced
   - [AppArmor](07-advanced/apparmor.md)
   - [SSH FIDO2](07-advanced/ssh-fido2.md)
   - [Optional controls](07-advanced/optional-controls.md)

Coverage checklist: [CONTROL-COVERAGE.md](CONTROL-COVERAGE.md)

Automation: [../ansible/README.md](../ansible/README.md)

Diagrams (Mermaid) appear where order matters: kit layers and playbook flow in the [root README](../README.md), anti-lockout SSH path here and in [ssh-service](02-access-control/ssh-service.md), MFA rollout in [ssh-mfa](02-access-control/ssh-mfa.md).
