# Admin identity and privilege boundaries

## Threat

A single shared `root` password over SSH is the highest-value credential on the box. If it leaks, an attacker owns everything. If everyone uses root daily, you also lose accountability: logs cannot tell Alice from Bob.

## Do

Create three groups that express intent, then one human admin user:

| Group | Intent |
|-------|--------|
| `sshaccess` | May authenticate to sshd |
| `elevated` | May use `sudo` |
| `switchroot` | May use `su` to root |

```bash
# On the target (as root, first session)
groupadd --system sshaccess
groupadd --system elevated
groupadd --system switchroot

useradd --create-home --shell /bin/bash \
  --groups sshaccess,elevated,switchroot admin

# Set a strong local password (for sudo/console — not for SSH login)
passwd admin

install -d -m 700 -o admin -g admin /home/admin/.ssh
# Paste your public key:
# nano /home/admin/.ssh/authorized_keys
chmod 600 /home/admin/.ssh/authorized_keys
chown admin:admin /home/admin/.ssh/authorized_keys
```

Limit `sudo` to the `elevated` group:

```bash
# /etc/sudoers.d/elevated — edit with visudo -f
%elevated ALL=(ALL:ALL) NOPASSWD:ALL
```

> Lab convenience uses passwordless sudo so Ansible can become root. In stricter environments, require a password or limit commands.

Limit `su`:

```bash
# Ensure pam_wheel is active for su (Debian often ships a commented line)
# /etc/pam.d/su — enable:
# auth required pam_wheel.so group=switchroot
```

## Why

Splitting SSH access from privilege escalation means a compromised low-privilege account that somehow got a shell still cannot elevate unless it is also in `elevated` / `switchroot`. Group names document intent better than “put everyone in sudo.”

## Verify

```bash
# From your laptop — should succeed
ssh admin@SERVER_IP 'id; sudo -n true && echo sudo_ok'

# Should fail once SSH hardening is applied
ssh root@SERVER_IP
```

Confirm groups:

```bash
getent group sshaccess elevated switchroot
```

## Rollback

```bash
# Keep a root console open first
usermod -aG sudo admin   # temporary emergency path on Debian
# Or restore snapshot
```

## Next

[ssh-service.md](ssh-service.md)
