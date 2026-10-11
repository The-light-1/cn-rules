#!/usr/bin/env python3
from __future__ import annotations

import ipaddress
import re
import sys
import urllib.request
from pathlib import Path

GEOSITE_URL = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.list"
GEOIP_URL = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/cn.list"
OUT = Path("cn-direct.txt")

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)*"
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)

def fetch(url: str) -> list[str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "glinet-cn-direct-builder/1.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8-sig").splitlines()

def clean_domain(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None

    # MetaCubeX domain behavior list commonly uses "+.example.com"
    if s.startswith("+."):
        s = s[2:]
    elif s.startswith("."):
        s = s[1:]

    s = s.strip().lower().rstrip(".")
    if not s:
        return None

    # GL.iNet subscription parser expects plain domains, IPv4 or IPv4 CIDR.
    # Drop anything that is not a plain ASCII/punycode domain.
    if not DOMAIN_RE.fullmatch(s):
        return None
    return s

def clean_ipv4(line: str) -> str | None:
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    try:
        if "/" in s:
            net = ipaddress.ip_network(s, strict=False)
            if net.version != 4:
                return None
            return str(net)
        ip = ipaddress.ip_address(s)
        if ip.version != 4:
            return None
        return str(ip)
    except ValueError:
        return None

def main() -> int:
    domains_raw = fetch(GEOSITE_URL)
    ips_raw = fetch(GEOIP_URL)

    seen = set()
    out = []

    for line in domains_raw:
        item = clean_domain(line)
        if item and item not in seen:
            seen.add(item)
            out.append(item)

    for line in ips_raw:
        item = clean_ipv4(line)
        if item and item not in seen:
            seen.add(item)
            out.append(item)

    OUT.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")

    domain_count = sum(1 for x in out if "/" not in x and not re.fullmatch(r"\d+(?:\.\d+){3}", x))
    ip_count = len(out) - domain_count
    print(f"Wrote {OUT}: {len(out)} total rules ({domain_count} domains, {ip_count} IPv4/IP-CIDR rules)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
