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
from ros2em.core.docker_builder import prepare_ports, generate_compose_content
from ros2em.utils.compose_utils import env_path, compose_file
from ros2em.utils.file_utils import write_compose_file, write_metadata

def init_env(name: str, distro: str, additional_ports: list[str] = None, context: str = "default"):
    env_dir = env_path(name)
    compose_path = compose_file(name)

    if compose_path.exists():
        print(f"[yellow]Environment '{name}' already exists.[/yellow]")
        return
    
    os.makedirs(env_dir, exist_ok = True)

    # Port mappings
    primary_port = prepare_ports()
    all_port_mappings = [f"{primary_port}:80"] + (additional_ports or [])
    compose = generate_compose_content(name, distro, all_port_mappings)

    write_compose_file(compose_path, compose)
    write_metadata(env_dir, {
        "name": name,
        "distro": distro,
        "vnc_port": primary_port,
        "extra_ports": additional_ports,
        "context": context
    })    

    print(f"[green]Environment '{name}' created with ROS 2 distro: {distro}[/green]")
    print(f"[blue]To start it, run:[/blue] ros2em up {name}")
    if additional_ports:
        print(f"[blue]Additional port mappings:[/blue] {', '.join(additional_ports)}")