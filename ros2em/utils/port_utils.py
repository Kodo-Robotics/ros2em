# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

import socket

def find_free_port(start_port = 6000, end_port = 7000):
    for port in range(start_port, end_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return port
            except OSError:
                continue
    
    raise RuntimeError("No free ports in range.")