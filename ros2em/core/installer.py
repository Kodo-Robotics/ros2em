# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import platform
import shutil
import subprocess
import urllib.request
import tempfile
import os
from tqdm import tqdm
from pathlib import Path
from rich import print
import typer

def is_installed(cmd):
    # Try path first
    if shutil.which(cmd):
        return True
    
    # Windows specific fallback for VirtualBox
    if platform.system() == "Windows" and cmd.lower() == "vboxmanage":
        default_path = Path("C:/Program Files/Oracle/VirtualBox/VBoxManage.exe")
        return default_path.exists()

    return False

def download_file(url, filename):
    tmp_dir = tempfile.gettempdir()
    path = os.path.join(tmp_dir, filename)
    print(f"[blue]Downloading {filename}...[/blue]")

    response = urllib.request.urlopen(url)
    total_size = int(response.getheader('Content-Length').strip())
    block_size = 1024 * 32 

    with open(path, 'wb') as f, tqdm(
        total = total_size, unit = 'B', unit_scale = True, desc = os.path.basename(path)
    ) as pbar:
        while True:
            buffer = response.read(block_size)
            if not buffer:
                break
            f.write(buffer)
            pbar.update(len(buffer))

    print(f"[green]Downloaded to {path}[/green]")
    return path

def install_virtualbox():
    system = platform.system()

    print("[blue]Installing VirtualBox...[/blue]")

    if system == "Windows":
        url = "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-Win.exe"
        path = download_file(url, "virtualbox.exe")
        print("[yellow]Launching VirtualBox installer...[/yellow]")
        subprocess.run([path])
    
    elif system == "Darwin":
        url = "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-OSX.dmg"
        path = download_file(url, "virtualbox.dmg")
        print(f"[yellow]Please open the .dmg file and install manually: {path}[/yellow]")
        subprocess.run(["open", path])

    elif system == "Linux":
        print("[yellow]Please install VirtualBox using your distro's package manager.[/yellow]")
    else:
        print("[red]Unsupported OS[/red]")

def install_vagrant():
    system = platform.system()
    arch = platform.machine()

    if system == "Windows":
        url = "https://releases.hashicorp.com/vagrant/2.4.1/vagrant_2.4.1_windows_amd64.msi"
        path = download_file(url, "vagrant.msi")
        print("[yellow]Launching Vagrant installer...[/yellow]")
        subprocess.run(["msiexec", "/i", path])
    
    elif system == "Darwin":
        if arch == "arm64":
            url = "https://releases.hashicorp.com/vagrant/2.4.1/vagrant_2.4.1_darwin_arm64.dmg"
        else:
            url = "https://releases.hashicorp.com/vagrant/2.4.1/vagrant_2.4.1_darwin_amd64.dmg"
        path = download_file(url, "vagrant.dmg")
        print(f"[yellow]Please open the .dmg file and install manually: {path}[/yellow]")
        subprocess.run(["open", path])
    
    elif system == "Linux":
        print("[yellow]Please install Vagrant using your distro's package manager.[/yellow]")
    else:
        print("[red]Unsupported OS[/red]")
    

def check_and_install_dependencies():
    print("[bold cyan]Checking dependencies...[/bold cyan]")

    vbox_installed = is_installed("VBoxManage")
    vagrant_installed = is_installed("vagrant")

    if vbox_installed:
        print("[green]✓ VirtualBox is installed.[/green]")
    else:
        print("[red]✗ VirtualBox not found.[/red]")
        if typer.confirm("Do you want to download and install VirtualBox now?"):
            install_virtualbox()

    if vagrant_installed:
        print("[green]✓ Vagrant is installed.[/green]")
    else:
        print("[red]✗ Vagrant not found.[/red]")
        if typer.confirm("Do you want to download and install Vagrant now?"):
            install_vagrant()
    
    if is_installed("VBoxManage") and is_installed("vagrant"):
        print("[bold green]All dependencies are now installed![/bold green]")
    else:
        print("[bold red]Some dependencies may still be missing. Please finish installation manually if prompted.[/bold red]")