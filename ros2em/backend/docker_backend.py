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
from pathlib import Path
from rich import print

from ros2em.utils.docker_utils import compose_file, write_compose_file, generate_compose_content
    
def init(name: str, path: Path, metadata: dict):
    compose_path = compose_file(name)
    if compose_path.exists():
        print(f"[yellow]Environment '{name}' already exists.[/yellow]")
        return
    
    distro = metadata.get("distro", "rolling")
    all_port_mappings = metadata.get("port_mappings", "6080:80")
    compose = generate_compose_content(name, distro, all_port_mappings)
    write_compose_file(compose_path, compose)

def up(name: str, path: Path, metadata: dict):
    compose_path = compose_file(name)
    if not compose_path.exists():
        print(f"[red]No such environment: {name}[/red]")
        return
    
    context = metadata.get("context", "default")
    if _container_exists(name):
        if _container_running(name):
            print(f"[green]Environment {name} is already running.[/green]")
        else:
            print(f"[yellow]Starting existing environment {name}...[/yellow]")
            subprocess.run(["docker", "--context", context, "start", name])
    else:
        print(f"[blue]Creating and starting new environment...[/blue]")
        subprocess.run(
            ["docker", "--context", context, "compose", "-f", str(compose_path), "up", "-d"], 
            cwd = path
        )

def stop(name: str, path: Path, metadata: dict):
    compose_path = compose_file(name)
    if not compose_path.exists():
        print(f"[red]No such environment: {name}[/red]")
        return
    
    context = metadata.get("context", "default")
    if _container_exists(name):
        if _container_running(name):
            subprocess.run(
                ["docker", "--context", context, "stop", name], 
                cwd = path
            )
            print(f"[green]Environment {name} stopped.[/green]")
        else:
            print(f"[yellow]Environment {name} is already stopped.[/yellow]")
    else:
        print(f"[red]Container {name} does not exist.[/red]")

def exec(name: str, cmd: list[str], capture: bool = False) -> str | None:
    result = subprocess.run(["docker", "exec", name] + cmd,
                            capture_output=capture, text=True)
    return result.stdout.strip() if capture and result.returncode == 0 else None

def _container_exists(name: str) -> bool:
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return f"{name}" in result.stdout

def _container_running(name: str) -> bool:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    return f"{name}" in result.stdout