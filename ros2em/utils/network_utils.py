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

import socket
from typing import List, Tuple
from rich import print

def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False

def find_available_port(start: int = 6080, end: int = 6100) -> int:
    for port in range(start, end):
        if is_port_available(port):
            return port
    raise RuntimeError("No available ports found in the range.")

def validate_ports_available(ports: List[int]) -> bool:
    for port in ports:
        if not is_port_available(port):
            print(f"[red]Port {port} is already in use. Cannot proceed.[/red]")
            return False
    return True

def prepare_ports() -> Tuple[int, list[str]]:
    primary_port = 6080
    if not is_port_available(primary_port):
        primary_port = find_available_port(start = 6081)
    return primary_port

def get_vnc_port(ports: List[str]) -> int:
    vnc_port = int(ports[0].split(":")[0])
    return vnc_port