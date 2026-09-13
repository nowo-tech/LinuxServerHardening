# Hardening the SSH service

## Threat

Default OpenSSH on port 22 with password authentication is the most scanned surface on the public Internet. Weak algorithms and root login multiply the blast radius of a single stolen password.

## Do

### Order of operations (critical)

1. Confirm key login as `admin` works on the **current** port.
2. Allow the **new** port in the firewall.
3. Change `sshd` settings.
4. Reload `sshd`.
5. Open a **second** SSH session before closing the first.

### Recommended policy (modern OpenSSH)

Create a drop-in file (cleaner than editing the whole `sshd_config`):

```bash
# /etc/ssh/sshd_config.d/10-nowo-hardening.conf
Port 2222
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AllowGroups sshaccess

LoginGraceTime 30
MaxAuthTries 3
MaxSessions 3
MaxStartups 10:30:60
ClientAliveInterval 300
ClientAliveCountMax 2

X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
AllowStreamLocalForwarding no
PermitTunnel no
GatewayPorts no
PermitEmptyPasswords no
PermitUserEnvironment no
HostbasedAuthentication no
IgnoreRhosts yes
Compression no
TCPKeepAlive no
DebianBanner no
UseDNS no
LogLevel VERBOSE

# Prefer strong host keys already present on the host
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key

# Modern algorithm sets for current OpenSSH
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256

Subsystem sftp internal-sftp -f AUTHPRIV -l INFO
```

Validate and reload:

```bash
sshd -t && systemctl reload ssh
```

### Trim weak Diffie-Hellman moduli

```bash
cp -a /etc/ssh/moduli /etc/ssh/moduli.bak
awk '$5 >= 3071' /etc/ssh/moduli.bak > /etc/ssh/moduli
sshd -t && systemctl reload ssh
```

### Optional: MFA

If you need a second factor, prefer `libpam-google-authenticator` or hardware keys **after** key-only SSH works. Add MFA in a dedicated change window; combining port changes + MFA + firewall in one sitting is a lock-out cocktail.

## Why

| Setting | Reason |
|---------|--------|
| Non-default port | Reduces noisy bots (not real security alone) |
| `AllowGroups` | Explicit allow-list of who may even attempt auth |
| No passwords | Removes online guessing against user passwords |
| No root login | Forces named admin accounts and cleaner audit trails |
| Forwarding off | Stops the box being used as a pivot by default |
| Strong moduli | Avoids weak DH groups in legacy key exchange |
| Explicit Kex/Ciphers/MACs | Drops legacy algorithms scanners still try |
| `LogLevel VERBOSE` | Records which key fingerprint authenticated |
| Audited SFTP subsystem | Keeps file-transfer actions in AUTHPRIV logs |

## Verify

```bash
# Must work
ssh -p 2222 -i ~/.ssh/lab_ed25519 admin@SERVER_IP

# Must fail
ssh -p 2222 root@SERVER_IP
ssh -p 22 admin@SERVER_IP

sshd -T | egrep 'port|permitrootlogin|passwordauthentication|allowgroups'
```

## Rollback

From console:

```bash
rm /etc/ssh/sshd_config.d/10-nowo-hardening.conf
mv /etc/ssh/moduli.bak /etc/ssh/moduli
systemctl reload ssh
```

## Next

[ssh-mfa.md](ssh-mfa.md) — optional second factor after keys work.
