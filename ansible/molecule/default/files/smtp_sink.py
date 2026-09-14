#!/usr/bin/env python3
"""Minimal SMTP sink for Molecule mail-path tests (no TLS, accepts anything)."""
from __future__ import annotations

import argparse
import socket
import sys


def handle(conn: socket.socket) -> None:
    conn.sendall(b"220 molecule-sink ESMTP\r\n")
    data_mode = False
    buf = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        buf += chunk
        while b"\r\n" in buf:
            line, buf = buf.split(b"\r\n", 1)
            text = line.decode("utf-8", "replace").strip()
            upper = text.upper()
            if data_mode:
                if text == ".":
                    data_mode = False
                    conn.sendall(b"250 OK\r\n")
                continue
            if upper.startswith("EHLO") or upper.startswith("HELO"):
                conn.sendall(b"250-molecule-sink\r\n250 OK\r\n")
            elif upper.startswith("MAIL") or upper.startswith("RCPT"):
                conn.sendall(b"250 OK\r\n")
            elif upper == "DATA":
                conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                data_mode = True
            elif upper in {"QUIT", "RSET"}:
                conn.sendall(b"221 Bye\r\n" if upper == "QUIT" else b"250 OK\r\n")
                if upper == "QUIT":
                    return
            else:
                conn.sendall(b"250 OK\r\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=2525)
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.host, args.port))
    sock.listen(5)
    sys.stderr.write(f"smtp-sink listening on {args.host}:{args.port}\n")
    sys.stderr.flush()
    while True:
        conn, _addr = sock.accept()
        with conn:
            try:
                handle(conn)
            except OSError:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
