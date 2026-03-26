"""API versioning helpers.

Keep a single source of truth for the current API version and prefix.
This makes it easy to add `/api/v2` later by adding a new module and wiring it.
"""

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"
