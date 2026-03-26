"""Optional secret loader (Vault/other secret stores).

The application can be configured to load secrets from an external vault at
startup. This is intentionally optional and disabled by default.

To enable:

    VAULT_URL=https://vault.example.com
    VAULT_TOKEN=...

Note: the current implementation uses a simple HTTP call and expects the vault
response to be JSON containing key/value pairs.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


def load_vault_secrets() -> None:
    """Load secrets from a vault endpoint and merge into os.environ."""

    if not settings.VAULT_URL or not settings.VAULT_TOKEN:
        return

    logger.info("Loading secrets from Vault: %s", settings.VAULT_URL)

    try:
        resp = requests.get(
            settings.VAULT_URL,
            headers={"Authorization": f"Bearer {settings.VAULT_TOKEN}"},
            timeout=10,
        )
        resp.raise_for_status()

        data: dict[str, Any] = resp.json()
        for k, v in data.items():
            if k in os.environ:
                continue
            os.environ[str(k)] = str(v)

        logger.info("Loaded %d secrets from Vault", len(data))
    except Exception as exc:
        logger.warning("Failed to load secrets from Vault: %s", exc)
