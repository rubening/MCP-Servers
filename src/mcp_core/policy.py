from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List


class PathPolicy:
    """Enforces directory access rules for filesystem-oriented tools."""

    def __init__(self, allowed_roots: Iterable[str | Path]) -> None:
        resolved = []
        for root in allowed_roots:
            path = Path(root).expanduser().resolve()
            resolved.append(path)
        if not resolved:
            raise ValueError("PathPolicy requires at least one allowed root")
        self._allowed: List[Path] = resolved

    def is_allowed(self, path: str | Path) -> bool:
        candidate = Path(path).expanduser().resolve()
        return any(candidate == root or candidate.is_relative_to(root) for root in self._allowed)

    def ensure_allowed(self, path: str | Path) -> Path:
        path_obj = Path(path).expanduser().resolve()
        if not self.is_allowed(path_obj):
            allowed_str = ", ".join(str(p) for p in self._allowed)
            raise PermissionError(f"Path '{path_obj}' is outside allowed roots: {allowed_str}")
        return path_obj

    def normalize(self, path: str | Path) -> str:
        return str(self.ensure_allowed(path))

    @classmethod
    def from_env(cls, env_var: str, fallback: Iterable[str | Path]) -> "PathPolicy":
        raw = os.environ.get(env_var)
        if raw:
            roots = [entry.strip() for entry in raw.split(os.pathsep) if entry.strip()]
            if roots:
                return cls(roots)
        return cls(fallback)
