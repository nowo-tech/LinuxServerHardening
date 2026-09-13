# Outbound mail for alerts

## Threat

A hardened server that cannot tell you it is under attack is only half useful. Local logs rotate; humans need a push channel.

## Do

Use a lightweight SMTP client such as `msmtp` with your provider’s submission port:

```bash
apt install -y msmtp msmtp-mta mailutils
```

`/etc/msmtprc` sketch:

```text
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        /var/log/msmtp.log

account        alerts
host           smtp.example.com
port           587
from           server-alerts@example.com
user           server-alerts@example.com
password       CHANGE_ME

account default : alerts
```

```bash
chmod 600 /etc/msmtprc
chown root:root /etc/msmtprc
touch /var/log/msmtp.log && chmod 600 /var/log/msmtp.log

echo 'root: security@example.com' >> /etc/aliases
newaliases || true

echo 'Hardening kit test message' | mail -s 'lab mail ok' security@example.com
```

Store the SMTP password in **Ansible Vault**, never in a committed plaintext file.

## Why

msmtp is small and predictable for outbound alerts. Full MTAs (Postfix, Exim) are powerful but add attack surface you do not need for “send me Fail2Ban mail.”

## Verify

Check the inbox and `/var/log/msmtp.log`. Confirm UFW allows the submission port outbound.

## Rollback

```bash
apt purge -y msmtp msmtp-mta
rm -f /etc/msmtprc
```

## Next

[log-digests.md](log-digests.md)
