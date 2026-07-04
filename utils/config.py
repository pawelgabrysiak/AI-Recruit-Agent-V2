import yaml
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"

def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
