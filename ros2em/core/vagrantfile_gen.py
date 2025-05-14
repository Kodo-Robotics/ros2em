# SPDX-FileCopyrightText: 2025 Kodo Robotics
#
# SPDX-License-Identifier: MIT

def generate_vagrantfile(env_path, name, host_ports, cpu, ram):
    content = f"""
Vagrant.configure("2") do |config|
    config.vm.define "{name}" do |vm|
        vm.vm.box = "ros2em/ros2-humble"
        vm.vm.hostname = "{name}"

        vm.vm.network "public_network"
        vm.vm.network "forwarded_port", guest: 6080, host: {host_ports['vnc']}, host_ip: "127.0.0.1"
        vm.vm.boot_timeout = 600
        
        vm.vm.provider "virtualbox" do |vb|
            vb.name = "{name}"
            vb.memory = "{ram}"
            vb.cpus = {cpu}
        end
    end
end
""".strip()
    
    with open(env_path / "Vagrantfile", "w") as f:
        f.write(content)