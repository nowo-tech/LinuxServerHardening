# Security principles

## Threat

Without principles, hardening becomes a random pile of settings. You will over-lock a lab box, under-lock a public VPS, or break your own access and “fix” it by weakening SSH again.

## Do

Write a one-page policy for **this** server (not the entire company). Example:

```text
Asset: billing-api-01 (Debian 13 VPS)
Data: customer PII in Postgres; TLS certs on disk
Admins: 2 people, key-only SSH from anywhere (travel)
Inbound: 443 (app), 2222 (SSH)
Outbound: 53, 80, 443, 123, 587
Must detect: brute force, unexpected listeners, rootkit signals
Must alert: mail to security@example.com within 15 minutes
```

Keep it short. Update it when the role of the machine changes.

## Why

Good baselines share a few ideas:

1. **Least privilege** — every account and process gets the minimum rights it needs.
2. **Defense in depth** — SSH hardening does not replace a firewall; a firewall does not replace patching.
3. **Fail closed** — when unsure, deny and open explicitly.
4. **Observable by default** — if you cannot see auth failures, you cannot react.
5. **Recoverable** — every change has a rollback and an out-of-band console path.

## Verify

Ask three questions about any new control:

- Does it reduce a real risk on **this** host?
- Can I prove it is active in under two minutes?
- If it fails at 3 a.m., can I recover without the person who enabled it?

## Rollback

If a principle document becomes outdated, replace it — do not accumulate contradictory rules. Archive the old page with a date so incident reviews stay honest.

## Next

[threat-model.md](threat-model.md)
