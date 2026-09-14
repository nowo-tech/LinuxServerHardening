# Log digests with logwatch

## Threat

Raw journals are easy to ignore. A daily digest forces a human (or a ticket) to see spikes in auth failures, disk errors, and daemon restarts.

## Do

Requires working outbound mail ([mail-alerts.md](../06-operations/mail-alerts.md)).

```bash
apt install -y logwatch

cat >/etc/cron.daily/00nowo-logwatch <<'EOF'
#!/bin/sh
exec /usr/sbin/logwatch --output mail --format html \
  --mailto security@example.com --range yesterday --service all
EOF
chmod 755 /etc/cron.daily/00nowo-logwatch
```

Tune `--service` lists on busy hosts to keep mail readable.

## Why

logwatch is a cheap “did anything weird happen yesterday?” layer. It is not real-time IDS; pair it with Fail2Ban/PSAD for that.

## Verify

```bash
logwatch --output stdout --format text --range today --service sshd | head
```

## Rollback

```bash
rm /etc/cron.daily/00nowo-logwatch
apt purge -y logwatch
```

## Next

[monitoring-and-healthchecks.md](monitoring-and-healthchecks.md) · [cicd-and-deploy.md](cicd-and-deploy.md) · [continuous-review.md](continuous-review.md)
