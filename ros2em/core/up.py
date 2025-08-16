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

import subprocess
from rich import print
from ros2em.utils.compose_utils import env_path, compose_file
from ros2em.utils.file_utils import read_metadata
from ros2em.utils.network_utils import validate_ports_available

def up_env(name: str):
    env_dir = env_path(name)
    compose_path = compose_file(name)

    if not compose_path.exists():
        print(f"[red]No such environment: {name}[/red]")
        return

    metadata = read_metadata(env_dir)
    context = metadata.get("context", "default")
    extra_ports = metadata.get("extra_ports", [])
    vnc_port = metadata.get("vnc_port", 6080)
    
    all_host_ports = [vnc_port] + [int(p.split(":")[0]) for p in extra_ports]
    if not validate_ports_available(all_host_ports):
        return

    subprocess.run(
        ["docker", "--context", context, "compose", "-f", str(compose_path), "up", "-d"], 
        cwd = env_dir
    )