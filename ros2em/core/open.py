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

from ros2em.utils.compose_utils import env_path
from ros2em.utils.file_utils import read_metadata
from rich import print
import webbrowser

def open_vnc(name: str):
    env_dir = env_path(name)
    metadata = read_metadata(env_dir)

    if not metadata:
        print(f"[red]No metadata found for environment '{name}'[/red]")
        return

    port = metadata.get("vnc_port")
    if not port:
        print(f"[red]No VNC port found in metadata for '{name}'[/red]")
        return
    
    url = f"http://localhost:{port}"
    print(f"[cyan]Opening VNC viewer at:[/cyan] {url}")
    webbrowser.open(url)