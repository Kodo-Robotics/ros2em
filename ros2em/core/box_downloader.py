# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import os
import platform
import subprocess
import gdown
from pathlib import Path
from rich import print

ROS2EM_HOME = Path.home() / ".ros2em"
BOX_DIR = ROS2EM_HOME / "boxes"

BOXES = {
    "ros2-humble": {
        "amd64": "1jnvDkELTvB8j5azmaAQNRagf9WPDtIZr",
        "arm64": "1yP6OsV9DLgnG4Qs1H632AxcGOpE-G0Qz"
    }
}

def get_arch():
    arch = platform.machine().lower()
    if arch in ("x86_64", "amd64"):
        return "amd64"
    elif arch in ("aarch64", "arm64"):
        return "arm64"
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

def download_and_register_box(box_name = "ros2-humble"):
    arch = get_arch()
    file_id = BOXES.get(box_name, {}).get(arch)

    if not file_id:
        print(f"[red]No box available for {box_name} on {arch}[/red]")
        return

    arch_box_dir = BOX_DIR / arch
    arch_box_dir.mkdir(parents = True, exist_ok = True)

    box_file = arch_box_dir / f"{box_name}.box"
    box_name_arch = f"ros2em/{box_name}"

    if box_file.exists():
        print(f"[yellow]Box file already exists at: {box_file}[/yellow]")
    else:
        print(f"[blue]Downloading {box_name} for {arch}...[/blue]")
        try:
            gdown.download(id = file_id, output = str(box_file), quiet = False)
            print(f"[green]Downloaded to {box_file}[/green]")
        except Exception as e:
            print(f"[red]Failed to download: {e}[/red]")
            return

    print(f"[blue]Registering box: {box_name_arch}[/blue]")
    try:
        subprocess.run(["vagrant", "box", "add", box_name_arch, str(box_file), "--force"], check = True)
        print(f"[green]Box {box_name_arch} added to Vagrant.[/green]")
    except:
        print(f"[red]Failed to add box '{box_name_arch}'[/red]")
