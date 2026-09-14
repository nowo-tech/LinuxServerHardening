# CI/CD and automated deploys onto hardened hosts

## Threat

Pipelines that “just SSH as root on port 22” fight this kit. Equally dangerous: CI runners that share the same IP as attackers and get Fail2Ban’d mid-deploy, or secrets pasted into plain job logs. Hosts without a controlled update path also tempt operators into ad-hoc `git pull` as root over SSH.

## Do

### Ansible deploy agents (idempotent)

The `deploy_agents` role **always** runs on harden. Each agent is independent:

| Variable | Default | When `true` | When `false` |
|----------|---------|-------------|--------------|
| `harden_enable_gha_runner` | `false` | Install + register + systemd GitHub Actions runner | Stop, unregister (if token set), purge home |
| `harden_enable_webhook_deploy` | `false` | Local push webhook → `git fetch/reset` + optional `systemctl restart` | Stop + remove unit/env/script |

```bash
# Self-hosted runner (needs vault_gha_runner_token + harden_gha_runner_url)
ansible-playbook -i inventories/prod/hosts.yml playbooks/02-harden.yml \
  --ask-vault-pass -e @profiles/prod.yml --tags gha_runner \
  -e harden_enable_gha_runner=true

# Push-to-deploy webhook (needs vault_webhook_deploy_secret + repo path)
ansible-playbook ... --tags webhook_deploy \
  -e harden_enable_webhook_deploy=true \
  -e harden_webhook_deploy_repo_path=/var/www/app \
  -e harden_webhook_deploy_branch=main \
  -e harden_webhook_deploy_restart_service=myapp

# Uninstall either agent
ansible-playbook ... --tags gha_runner -e harden_enable_gha_runner=false
```

#### GitHub Actions self-hosted runner

1. In GitHub → Settings → Actions → Runners → **New self-hosted runner** → copy the registration token into `vault_gha_runner_token`.
2. Set `harden_gha_runner_url` to the repo or org URL (not `REPLACE_ME_*`).
3. Pin `harden_gha_runner_version` (default `2.337.0`); optional `harden_gha_runner_checksum`.
4. Prefer labels like `self-hosted,linux,debian,prod` and target jobs with `runs-on:`.
5. Runner listens **outbound** to GitHub — no inbound UFW hole required.

#### Webhook auto-deploy (push → update code)

1. Put a HMAC secret in `vault_webhook_deploy_secret`.
2. Point `harden_webhook_deploy_repo_path` at an existing clone, **or** set `harden_webhook_deploy_repo_url` to clone once.
3. Default listen `127.0.0.1:9000` — put nginx/Caddy with TLS in front, or set `harden_webhook_deploy_ufw_allow: true` and allowlist GitHub hooks (better: reverse proxy).
4. In GitHub → Webhooks: URL `https://host/hooks/deploy`, content type JSON, secret = vault secret, event **push**.
5. Optional `harden_webhook_deploy_restart_service` restarts a systemd unit after `git reset --hard origin/<branch>`.

Health: `GET /hooks/deploy/healthz` → `ok`.

```mermaid
flowchart LR
  Push[git push] --> GH[GitHub / Gitea]
  GH -->|Actions job| Runner[GHA self-hosted runner]
  GH -->|HMAC webhook| Hook[nowo-webhook-deploy]
  Runner --> Host[(Debian host)]
  Hook -->|git reset --hard| Repo[/var/www/app]
  Hook -->|optional| Svc[systemctl restart]
```

### What this repository’s own CI already does

| Piece | Role |
|-------|------|
| GitHub Actions (this kit repo) | Syntax, yamllint, ansible-lint, Molecule — **not** production deploys |
| `01-bootstrap` / `02-harden` / `03-audit` | Operator-driven from a control node with Vault |

Treat **kit CI** as quality gates for the playbooks. Treat **your app CD** as runners/webhooks above (or SSH from a pipeline).

### Inventory and SSH for remote deploy jobs

1. Use the **runtime** inventory (`ansible_user=admin`, hardened port).
2. Dedicated deploy key / runner user — not your interactive MFA admin.
3. Put **stable** runner egress / webhook reverse-proxy IPs in Fail2Ban `ignoreip`.

### Suggested CD health gate

```bash
curl -fsS --retry 5 --retry-all-errors --max-time 10 \
  "https://${APP_HOST}/healthz" >/dev/null
```

### What not to automate from CD

- Interactive MFA enrolment
- Blind `ufw reset`
- Enabling PSAD `AUTO_IDS` or passwordless sudo “so the pipeline is easier”
- Exposing the webhook on `0.0.0.0` without TLS + secret + allowlist

## Why

Hardening and delivery share SSH, firewall, and trust. Shipping **opt-in runners/webhooks** lets a push update code without weakening the baseline — and `enable: false` removes the attack surface again.

## Verify

```bash
# Runner
systemctl is-active actions.runner.nowo
# Webhook
systemctl is-active nowo-webhook-deploy
curl -fsS http://127.0.0.1:9000/hooks/deploy/healthz
# After disable flags + re-run --tags deploy:
test ! -e /etc/systemd/system/nowo-webhook-deploy.service
test ! -e /opt/actions-runner/run.sh
```

## Rollback

Set `harden_enable_gha_runner` / `harden_enable_webhook_deploy` to `false` and re-run `--tags deploy`. Revoke the GitHub registration token and delete the webhook in the repo settings.

## Next

[monitoring-and-healthchecks.md](monitoring-and-healthchecks.md) · [continuous-review.md](continuous-review.md) · [../../ansible/README.md](../../ansible/README.md)
