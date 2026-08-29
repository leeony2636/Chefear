"""Load local environment variables without storing secrets in the repository."""

from pathlib import Path
import os


def load_env(env_path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from a local .env file if one exists."""
    env_path = env_path or (Path(__file__).resolve().parents[1] / ".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())
