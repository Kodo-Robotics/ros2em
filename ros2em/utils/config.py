# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import json
from pathlib import Path

def write_config(env_path: Path, config: dict):
    with open(env_path / "ros2em.json", "w") as f:
        json.dump(config, f, indent = 2)

def read_config(env_path: Path) -> dict:
    config_file = env_path / "ros2em.json"
    if not config_file.exists():
        return {}
    
    with open(config_file, "r") as f:
        return json.load(f)