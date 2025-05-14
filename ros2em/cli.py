# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import typer
from ros2em.core import env_manager, installer, box_downloader
from rich import print

app = typer.Typer(help = "ros2em: ROS2 Environment Manager")

@app.command()
def init():
    """Install dependencies (VirtualBox, Vagrant) if needed."""
    installer.check_and_install_dependencies()

@app.command()
def download_box():
    """Download and register ROS2 box files."""
    box_downloader.download_and_register_box()

@app.command()
def create(
    name: str,
    cpu: int = typer.Option(2, help="Number of CPU cores"),
    ram: int = typer.Option(2048, help="RAM in MB")
):
    """Create new ROS2 VM environment."""
    env_manager.create_environment(name, cpu, ram)

@app.command()
def open(name: str):
    """Open the environment GUI in browser"""
    env_manager.open_environment(name)

@app.command()
def list():
    """List all environments and their status."""
    env_manager.list_environments()

@app.command()
def status(name: str):
    """Check the status of an environment"""
    env_manager.status_environment(name)

@app.command()
def start(name: str):
    """Start an existing environment."""
    env_manager.start_environment(name)

@app.command()
def stop(name: str):
    """Stop a running environment."""
    env_manager.stop_environment(name)

@app.command()
def delete(name: str):
    """Delete an environment."""
    env_manager.delete_environment(name)

if __name__ == "__main__":
    app()