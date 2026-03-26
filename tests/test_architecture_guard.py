from __future__ import annotations

from scripts.check_architecture import main


def test_architecture_guard_passes_for_current_repo_state() -> None:
    assert main() == 0
