# File integrity with AIDE

## Threat

Rootkits and quiet intruders alter binaries and configs without noisy SSH failures. If you only watch auth logs, you miss “the binary changed last Tuesday.”

## Do

```bash
apt install -y aide aide-common
# Enable daily cron in /etc/default/aide → CRON_DAILY_RUN=yes

aideinit
# After the initial DB is built, promote it (aideinit -y -f on Debian helpers)
```

After **intentional** system changes (package upgrades, config edits you approve):

```bash
aideinit -y -f    # or aide --update && move the new DB into place
```

Treat unexplained AIDE mail as an incident until proven otherwise.

## Why

AIDE is a host-based integrity sensor. It does not block attacks; it shortens time-to-detect. Pair it with auditd watches on identity files for complementary signals.

## Verify

```bash
aide.wrapper --check | head
ls -l /var/lib/aide/
```

## Rollback

```bash
rm -f /etc/cron.daily/*aide* 2>/dev/null || true
apt purge -y aide aide-common
```

## Next

[scanners.md](scanners.md)
