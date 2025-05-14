# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import os
import subprocess
import webbrowser
from pathlib import Path
from rich import print
from rich.text import Text
from rich.table import Table
from ros2em.core.vagrantfile_gen import generate_vagrantfile
from ros2em.utils.config import write_config, read_config
from ros2em.utils.port_utils import find_free_port

ROS2EM_HOME = Path.home() / ".ros2em"

def create_environment(name: str, cpu: int = 2, ram: int = 2048):
    env_path = ROS2EM_HOME / name
    if env_path.exists():
        print(f"[red]Environment '{name}' already exists.[/red]")
        return

    print(f"[green]Creating environment: {name}[/green]")
    os.makedirs(env_path, exist_ok = True)

    # Generate Vagrantfile
    host_ports = {"vnc": find_free_port(6080, 6100)}
    config = {
        "host_ports": host_ports,
        "resources": {"cpu": cpu, "ram": ram}
    }

    write_config(env_path, config)
    generate_vagrantfile(env_path, name, host_ports, cpu, ram)

    # Start the VM
    try:
        subprocess.run(["vagrant", "up"], cwd = env_path, check = True)
        print(f"[green]Environment '{name}' created and running.[/green]")
    except subprocess.CalledProcessError:
        print(f"[red]Failed to start VM for '{name}'.[/red]")

def open_environment(name: str):
    env_path = ROS2EM_HOME / name
    if not env_path.exists():
        print(f"[red]Environment '{name}' does not exist.[/red]")
        return
    
    config = read_config(env_path)
    vnc_port = config.get("host_ports", {}).get("vnc")

    if not vnc_port:
        print(f"[red]No VNC port configured for '{name}'.[/red]")
        return
    
    url = f"http://localhost:{vnc_port}"
    print(f"[blue]Opening environment '{name}' in browser: {url}[/blue]")
    webbrowser.open(url)

def list_environments():
    print("[blue]Fetching environments...[/blue]")

    try:
        result = subprocess.run(
            ["vagrant", "global-status", "--prune"],
            capture_output = True, text = True, check = True
        )
    except subprocess.CalledProcessError as e:
        print("[red]Error fetching global status.[/red]")
        return
    
    table = Table(title = "ROS2 Environments")
    table.add_column("Name", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("CPU", justify="center")
    table.add_column("RAM (MB)", justify="center")
    table.add_column("Open in Browser", justify="left")

    lines = result.stdout.strip().splitlines()
    parsing = False
    for line in lines:
        # Start parsing after header is detected
        if not parsing:
            if "id" in line and "name" in line and "provider" in line:
                parsing = True
            continue
        
        # Stop parsing if we reach footer
        if line.strip() == "":
            break

        parts = line.split()
        if len(parts) < 5:
            continue

        vm_id, name, provider, state = parts[:4]
        path = " ".join(parts[4:])
        if ROS2EM_HOME.name not in path:
            continue        
        
        # Generate URL
        vm_folder = Path(path).name
        config = read_config(Path(path))
        resources = config.get("resources", {})

        vnc_port = config.get("host_ports", {}).get("vnc")
        cpu = str(resources.get("cpu", "-"))
        ram = str(resources.get("ram", "-"))

        if vnc_port:
            vnc_url = f"http://localhost:{vnc_port}"
        else:
            vnc_url = "-"

        # Modify state
        if state == "running":
            status_display = Text("🟢 running", style="green")
        elif state == "poweroff":
            status_display = Text("🔴 poweroff", style="red")
        else:
            status_display = Text(state)

        table.add_row(vm_folder, status_display, cpu, ram, vnc_url)

    print(table)

def status_environment(name: str):
    env_path = ROS2EM_HOME / name
    if not env_path.exists():
        print(f"[red]Environment '{name}' does not exist.[/red]")
        return
    
    print(f"[cyan]Fetching status for '{name}'...[/cyan]")

    # Read port mapping
    config = read_config(env_path)
    vnc_port = config.get("host_ports", {}).get("vnc", "-")
    resources = config.get("resources", {})
    cpu = resources.get("cpu", "-")
    ram = resources.get("ram", "-")

    # Get status
    try:
        result = subprocess.run(
            ["vagrant", "status"],
            cwd = env_path,
            capture_output = True,
            text = True,
            check = True
        )
    except subprocess.CalledProcessError:
        print(f"[red]Failed to get status for '{name}'.[/red]")
        return
    
    # Parse status
    status_line = next(
        (line for line in result.stdout.splitlines() if line.strip().startswith("default")),
        None
    )

    status = "unknown"
    if status_line:
        parts = status_line.split()
        if len(parts) >= 2:
            status = parts[1]
    
    print()
    print(f"[bold green]{name}[/bold green] [dim]@ {env_path}[/dim]")
    print(f"[bold]Status:[/bold] {status}")
    print(f"[bold]CPU:[/bold] {cpu}")
    print(f"[bold]RAM:[/bold] {ram} MB")
    print(f"[bold]VNC Port:[/bold] {vnc_port}")
    print()

def start_environment(name: str):
    env_path = ROS2EM_HOME / name
    if not env_path.exists():
        print(f"[red]Environment '{name}' does not exist.[/red]")
        return
    
    print(f"[green]Starting environment '{name}'...[/green]")
    subprocess.run(["vagrant", "up"], cwd = env_path)

def stop_environment(name: str):
    env_path = ROS2EM_HOME / name
    if not env_path.exists():
        print(f"[red]Environment '{name}' does not exist.[/red]")
        return
    
    print(f"[yellow]Stopping environment '{name}'...[/yellow]")
    subprocess.run(["vagrant", "halt"], cwd = env_path)

def delete_environment(name: str):
    env_path = ROS2EM_HOME / name
    if not env_path.exists():
        print(f"[red]Environment '{name}' does not exist.[/red]")
        return
    
    print(f"[red]Deleting environment '{name}'...[/red]")
    subprocess.run(["vagrant", "destroy", "-f"], cwd = env_path)
    try:
        import shutil
        shutil.rmtree(env_path)
        print(f"[green]Environment '{name}' deleted.[/green]")
    except Exception as e:
        print(f"[red]Failed to delete folder: {e}[/red]")
