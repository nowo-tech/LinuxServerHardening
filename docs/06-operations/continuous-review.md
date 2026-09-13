# Continuous review and day-2 operations

## Threat

Hardening decays. New packages reopen ports, temporary firewall rules become permanent, and “just for debugging” SSH forwards linger for months.

## Do

### Monthly checklist

```text
[ ] ansible-playbook playbooks/03-audit.yml (or lynis audit system)
[ ] Review ufw status numbered — unexpected allows?
[ ] ss -tulpen — unexpected listeners?
[ ] fail2ban-client status — sane ban counts?
[ ] unattended-upgrade logs — failures?
[ ] Rotate or revoke admin SSH keys that left the team
[ ] Confirm backup restore still works (out of band)
[ ] If Docker is in use, re-check DOCKER-USER vs published ports
[ ] AIDE/rkhunter/chkrootkit mail — unexplained changes?
```

### Lynis-style system audit

```bash
apt install -y lynis
lynis audit system
less /var/log/lynis-report.dat
```

Treat suggestions as a backlog, not a shame score. Prioritise items that map to your threat model.

### Listening sockets

```bash
ss -tulpen
# Investigate anything you cannot name
```

### When you install a new app

1. Update the threat model inbound/outbound table
2. Add firewall rules **before** binding to `0.0.0.0`
3. Add Fail2Ban jails if the app has auth logs
4. Re-run the harden play with tags for firewall/mail only

## Why

Security is a loop: baseline → operate → observe → adjust. Automation keeps the baseline honest; humans still own exceptions.

## Verify

Pick last month’s Lynis report and confirm at least three findings were either fixed or explicitly accepted in writing.

## Rollback

Not applicable — this chapter is operational habit. If a playbook run causes pain, use each role’s rollback section and your VM snapshot.

## Next

Return to [../../ansible/README.md](../../ansible/README.md) and automate what you just practiced.
