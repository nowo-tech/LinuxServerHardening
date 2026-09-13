# SSH hardware keys (FIDO2)

## Threat

A software private key on disk can be copied if the laptop is compromised. A FIDO2 key keeps the private material in hardware and usually requires a touch (and optional PIN).

## Do

### On the admin workstation

```bash
# Generate a resident or non-resident sk key (OpenSSH 8.2+)
ssh-keygen -t ed25519-sk -O resident -O verify-required -f ~/.ssh/id_ed25519_sk -C "admin@yubikey"
```

Copy the `.pub` file to the server `authorized_keys` (or set `harden_ssh_public_key_path` to that pubkey for Ansible). Prefer `harden_ssh_keys_exclusive: true` after you confirm login works, so old software keys disappear.

### Server requirements

- OpenSSH recent enough to advertise `sk-ssh-ed25519@openssh.com` (Debian 12/13 is fine).
- Keep a **backup** admin path (second key or console) before removing software keys.

### Optional AuthenticationMethods

If you combine hardware key + TOTP:

```text
AuthenticationMethods publickey,keyboard-interactive
PubkeyAuthentication yes
KbdInteractiveAuthentication yes
```

Enrol TOTP first with `nullok`, then enforce (see [ssh-mfa.md](../02-access-control/ssh-mfa.md)).

## Why

Phishing-resistant admin auth beats “passwordless sudo + software key in Downloads.” FIDO2 fails closed when the token is absent.

## Verify

```bash
ssh -i ~/.ssh/id_ed25519_sk -p 2222 admin@SERVER
# Touch the token when prompted
```

## Rollback

Re-add a software pubkey via console, or restore from snapshot.

## Next

[optional-controls.md](optional-controls.md)
