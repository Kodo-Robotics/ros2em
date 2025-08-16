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

import typer
from ros2em.core import manager

app = typer.Typer(help = "ros2em: ROS2 Environment Manager")

@app.command()
def init(name: str = typer.Argument(..., help="Name of the environment"),
         distro: str = typer.Argument(..., help="ROS2 distro (e.g. humble, iron)"),
         ports: list[str] = typer.Option(None, "--ports", help="Extra port mappings (host:container)"),
         context: str = typer.Option("default", "--context", help="Docker context to use")
        ):
    """Create a new ROS2 environment"""
    manager.init_env(name, distro, ports, context)

@app.command()
def up(name: str = typer.Argument(..., help="Name of the environment")):
    """Start or activate the environment"""
    manager.up_env(name)

@app.command()
def stop(name: str = typer.Argument(..., help="Name of the environment")):
    """Stop or deactivate the environment."""
    manager.stop_env(name)

if __name__ == "__main__":
    app()