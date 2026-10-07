from __future__ import annotations

import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx

from .models import ResponseSnapshot, TLSInfo


class CollectionError(RuntimeError):
    pass


def normalize_url(url: str) -> str:
    value = url.strip()
    if not value:
        raise ValueError("Target URL cannot be empty")
    if "://" not in value:
        return f"https://{value}"
    return value


def collect_tls_info(url: str, timeout: float = 5.0) -> TLSInfo:
    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        return TLSInfo(enabled=False)

    host = parsed.hostname
    if not host:
        return TLSInfo(enabled=True, error="Unable to determine host")
    port = parsed.port or 443

    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as raw_sock:
            with context.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
                cert = tls_sock.getpeercert()
                cipher = tls_sock.cipher()
                protocol = tls_sock.version()

        not_after = cert.get("notAfter")
        expires_at = None
        days_until_expiry = None
        if not_after:
            expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            expires_at = expiry.isoformat()
            days_until_expiry = (expiry - datetime.now(timezone.utc)).days

        return TLSInfo(
            enabled=True,
            protocol=protocol,
            cipher=cipher[0] if cipher else None,
            expires_at=expires_at,
            days_until_expiry=days_until_expiry,
        )
    except Exception as exc:  # noqa: BLE001 - we preserve the diagnostic for the report
        return TLSInfo(enabled=True, error=str(exc))


def collect(url: str, timeout: float = 10.0, verify_tls: bool = True) -> ResponseSnapshot:
    target = normalize_url(url)
    headers = {
        "User-Agent": "CyberQuality-Static-Assessor/0.1",
        "Origin": "https://assessment.invalid",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    }

    try:
        with httpx.Client(
            follow_redirects=True,
            timeout=timeout,
            verify=verify_tls,
            headers=headers,
        ) as client:
            response = client.get(target)
    except httpx.HTTPError as exc:
        raise CollectionError(f"Unable to request {target}: {exc}") from exc

    header_map = {key.lower(): value for key, value in response.headers.items()}
    set_cookie_headers = response.headers.get_list("set-cookie")
    final_url = str(response.url)

    return ResponseSnapshot(
        target_url=target,
        final_url=final_url,
        status_code=response.status_code,
        headers=header_map,
        set_cookie_headers=set_cookie_headers,
        elapsed_ms=response.elapsed.total_seconds() * 1000,
        collected_at=datetime.now(timezone.utc).isoformat(),
        tls=collect_tls_info(final_url, timeout=min(timeout, 5.0)),
    )
