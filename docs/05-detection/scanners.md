# Malware and rootkit scanners

## Threat

Not every compromise looks like a failed SSH login. Persistence implants, webshells, and classic rootkits may sit quietly. Periodic scanners raise the chance you notice.

## Do

### ClamAV (signature AV)

```bash
apt install -y clamav clamav-daemon clamav-freshclam
systemctl enable --now clamav-freshclam
# Wait for signatures once
freshclam || true
```

Nightly scan example (exclude pseudo-filesystems):

```bash
# /etc/cron.d/clamav-nightly
30 3 * * * root /usr/bin/clamscan -r -i --exclude-dir="^/sys|^/proc|^/dev|^/run" / > /var/log/clamav/nightly.log 2>&1
```

### rkhunter

```bash
apt install -y rkhunter
rkhunter --update
rkhunter --propupd
rkhunter --check --sk
```

Enable daily cron via `/etc/default/rkhunter` (`CRON_DAILY_RUN="true"`).

### Reality check

AV on Linux catches known Linux malware and phishing drops stored on the box; it will not replace patching or least privilege. Tune aggressively against false positives on deploy directories.

## Why

Layered detection: Fail2Ban sees auth noise, auditd sees config tampering, ClamAV/rkhunter catch file-level oddities. Each sensor fails differently — together they cover more failure modes.

## Verify

```bash
clamscan --version
rkhunter --version
tail -n 50 /var/log/clamav/nightly.log
```

## Rollback

```bash
rm /etc/cron.d/clamav-nightly
systemctl disable --now clamav-daemon clamav-freshclam
apt purge -y clamav clamav-daemon rkhunter
```

## Next

[../06-operations/mail-alerts.md](../06-operations/mail-alerts.md)
