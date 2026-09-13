# Updates and password quality

## Threat

Unpatched OpenSSH, OpenSSL, or kernel CVEs are how “quiet” servers get owned months after install. Weak local passwords matter for console, `sudo`, and any service that still uses PAM.

## Do

### Unattended security updates

```bash
apt install -y unattended-upgrades apt-listchanges

dpkg-reconfigure -plow unattended-upgrades
```

Minimal policy file:

```text
# /etc/apt/apt.conf.d/50unattended-upgrades (excerpt)
Unattended-Upgrade::Origins-Pattern {
    "origin=Debian,codename=${distro_codename}-security";
};
# Kit default is false — enable only on disposable labs
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "04:30";
Unattended-Upgrade::Mail "security@example.com";
```

For disposable labs you may set reboot to `"true"` or use Ansible `profiles/lab.yml` (`harden_auto_reboot: true`). On production clusters, keep it **off** and schedule restarts yourself.

### apticron and apt-listchanges

```bash
apt install -y apticron apt-listchanges
# /etc/apticron/apticron.conf
EMAIL="security@example.com"
NOTIFY_NO_UPDATES="1"
```

apticron mails you about pending upgrades even when unattended-upgrades already handles security pockets — useful visibility for manual review packages.

### Password quality via PAM

```bash
apt install -y libpam-pwquality
```

Example `/etc/security/pwquality.conf` knobs:

```text
minlen = 12
dcredit = -1
ucredit = -1
lcredit = -1
ocredit = -1
maxrepeat = 3
difok = 4
dictcheck = 1
```

Ensure `pam_pwquality.so` is referenced from `/etc/pam.d/common-password`.

## Why

Security origins limit surprise. Feature freezes in `stable` already reduce churn; security pockets fix known holes. Password quality does not help SSH if passwords are disabled — it still protects local escalation and recovery workflows.

## Verify

```bash
unattended-upgrade --dry-run --debug 2>&1 | tail -20
grep pam_pwquality /etc/pam.d/common-password
# Try setting a bad password for a test user — it should be rejected
```

## Rollback

```bash
# Disable auto upgrades
echo 'APT::Periodic::Unattended-Upgrade "0";' > /etc/apt/apt.conf.d/20auto-upgrades.disable
# Revert pam line from backup
```

## Next

[kernel-and-sysctl.md](kernel-and-sysctl.md)
