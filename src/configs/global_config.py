import json

from pathlib import Path


CONFIG_DIR = Path.home() / ".claudio"

CONFIG_PATH = CONFIG_DIR / "config.json"


DEFAULT_CONFIG = {
    "model": "qwen3.5:4b",
}


def load_config():

    CONFIG_DIR.mkdir(exist_ok=True)

    if not CONFIG_PATH.exists():

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG

    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def save_config(config):

    CONFIG_DIR.mkdir(exist_ok=True)

    with open(CONFIG_PATH, "w") as file:

        json.dump(
            config,
            file,
            indent=4
        )