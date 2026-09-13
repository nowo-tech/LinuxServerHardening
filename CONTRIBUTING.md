# Contributing

Thanks for improving **Linux Server Hardening**.

## Rules of the road

1. **Teach, then automate.** Every new control needs a docs page with Threat / Do / Why / Verify / Rollback before (or with) the Ansible role.
2. **Keep secrets out of git.** Use Vault examples (`*.example`) only.
3. **Prefer drop-in files** (`sshd_config.d`, `sysctl.d`, `cron.d`) over rewriting entire vendor configs.
4. **Debian 12/13 first.** Note if a change is Ubuntu-specific.
5. **No lock-out recipes.** SSH and firewall changes must document console recovery.
6. **Diagrams sparingly.** Prefer Mermaid only for multi-step flows (bootstrap/harden, SSH cutover, MFA rollout). Single-control chapters stay Threat/Do/Why text.

## Pull requests

- Small, focused PRs beat giant rewrites.
- Name roles and variables with the `harden_` / Nowo prefixes already used.
- Run `ansible-playbook --syntax-check` on touched plays.

## Tone

Documentation is English, direct, and example-heavy. Avoid fear-mongering; explain trade-offs.
