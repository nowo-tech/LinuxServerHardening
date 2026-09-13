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

Nightly scan example — **scope paths** (full `/` is brutal on small VPS disks):

```bash
# /etc/cron.d/nowo-clamav-nightly
30 3 * * * root /usr/bin/clamscan -r -i \
  --exclude-dir="^/sys|^/proc|^/dev|^/run" \
  /home /var/www /tmp /opt >> /var/log/clamav/nightly.log 2>&1
```

Ansible uses `harden_clamav_scan_paths` the same way (`harden_enable_clamav: true`).

### rkhunter

```bash
apt install -y rkhunter
rkhunter --update
rkhunter --propupd
rkhunter --check --sk
```

Enable daily cron via `/etc/default/rkhunter` (`CRON_DAILY_RUN="true"`).

### chkrootkit (second opinion)

```bash
apt install -y chkrootkit
chkrootkit
# Enable daily run via /etc/chkrootkit.conf when the package ships cron hooks
```

Use chkrootkit **and** rkhunter as independent signatures; do not treat a clean run of one as proof.

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
rm /etc/cron.d/nowo-clamav-nightly
systemctl disable --now clamav-daemon clamav-freshclam
apt purge -y clamav clamav-daemon rkhunter
```

## Next

[../06-operations/mail-alerts.md](../06-operations/mail-alerts.md)
