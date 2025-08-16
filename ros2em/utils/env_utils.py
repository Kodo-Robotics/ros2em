# Copyright (c) 2025 Kodo Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.cwd()

def env_path(name: str) -> Path:
    return BASE_DIR / name

def write_metadata(path: Path, metadata: dict):
    metadata["created_at"] = datetime.now().isoformat()
    with open(path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent = 2)

def read_metadata(env_path: Path) -> dict:
    meta_file = env_path / "metadata.json"
    if not meta_file.exists():
        return {}
    
    with open(meta_file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}