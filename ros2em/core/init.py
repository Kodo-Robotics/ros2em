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

import os
from rich import print

from ros2em.backend import docker_backend
from ros2em.utils.network_utils import prepare_ports
from ros2em.utils.env_utils import env_path, read_metadata, write_metadata

def init_env(name: str, distro: str, additional_ports: list[str] = None, context: str = "default"):
    env_dir = env_path(name)
    os.makedirs(env_dir, exist_ok = True)

    # Port mappings
    primary_port = prepare_ports()
    all_port_mappings = [f"{primary_port}:80"] + (additional_ports or [])
    write_metadata(env_dir, {
        "name": name,
        "distro": distro,
        "port_mappings": all_port_mappings,
        "context": context
    })

    metadata = read_metadata(env_dir)
    docker_backend.init(name, env_dir, metadata)    

    print(f"[green]Environment '{name}' created with ROS 2 distro: {distro}[/green]")
    print(f"[blue]To start it, run:[/blue] ros2em up {name}")
    if additional_ports:
        print(f"[blue]Additional port mappings:[/blue] {', '.join(additional_ports)}")