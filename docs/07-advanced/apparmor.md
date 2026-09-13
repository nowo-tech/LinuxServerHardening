# AppArmor on Debian

## Threat

Even a patched daemon can be abused through a bug. Without Mandatory Access Control, a compromised process keeps the full rights of its user (often root for system services).

## Do

Debian ships AppArmor enabled on many images. Check status:

```bash
aa-status
systemctl status apparmor
```

Enforce profiles that already exist for tools you run:

```bash
apt install -y apparmor-utils
# Example — only if the profile is present and tested:
# aa-enforce /etc/apparmor.d/usr.sbin.ntpd
aa-status
```

For custom apps, start in complain mode, fix denials, then enforce:

```bash
aa-complain /etc/apparmor.d/local/my-service
# exercise the service, review dmesg / journal
aa-enforce /etc/apparmor.d/local/my-service
```

Do **not** blindly enforce every profile on day one — broken profiles lock out daemons.

## Why

AppArmor is the practical MAC default on Debian/Ubuntu. It complements (does not replace) firewall, SSH hardening, and least privilege.

## Verify

```bash
aa-status | head
journalctl -k | grep -i apparmor | tail
```

## Rollback

```bash
aa-disable /etc/apparmor.d/PATH_TO_PROFILE
# or boot with apparmor=0 only as emergency recovery
```

## Next

[ssh-fido2.md](ssh-fido2.md)
