# ros2em - ROS2 Environment Manager

[![PyPI version](https://img.shields.io/pypi/v/ros2em.svg)](https://pypi.org/project/ros2em/)
[![License](https://img.shields.io/github/license/Kodo-Robotics/ros2em.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-blue)](#)

**ros2em** is a CLI tool to create and manage isolated ROS2 environments using VirtualBox and Vagrant.

Whether you're a robotics developer, student, or researcher, `ros2em` makes it easy to:

* 🧠 Launch ROS2 in clean, isolated virtual machines
* 🖥 Access GUIs like Rviz or Gazebo via browser
* ✅ Support both `amd64` and `arm64` architectures
* 🧰 Handle setup: VirtualBox, Vagrant, and box file download

---

## 🚀 Features

* ⚡ One-line setup for fully functional ROS 2 VMs
* 📦 Architecture-specific box handling (`amd64`, `arm64`)
* 🖥 GUI access using browser
* 🔐 No system pollution – nothing touches your host machine
* 💡 Powered by Typer (CLI) and Rich (colored output)

---

## 📦 Installation

### Recommended (via pipx)

```bash
pipx install ros2em
```

### Or using pip

```bash
pip install ros2em
```

---

## 🛠 Commands

### 🔧 Setup dependencies

```bash
ros2em init
```

Installs VirtualBox and Vagrant (if not found).

### ⬇️ Download the correct ROS2 box

```bash
ros2em download-box
```

Auto-detects your architecture and downloads the appropriate `.box` file.

### 🐢 Create an environment

```bash
ros2em create myenv
```

Creates `~/.ros2em/myenv` and spins up a VM.

### 📋 Manage environments

```bash
ros2em list        # List all environments
ros2em start myenv # Start a VM
ros2em stop myenv  # Stop a VM
ros2em delete myenv # Delete an environment
```

---

## 📁 Environment Structure

```
~/.ros2em/
├── boxes/
│   └── arm64/ or amd64/
│       └── ros2-humble.box
├── myenv/
│   └── Vagrantfile
```

---

## 🧩 Contributing

We welcome contributions, ideas, and feedback.

* [ ] Open issues for bugs and enhancements
* [ ] Fork and submit a pull request
* [ ] Share your use case via Discussions

---

## 📄 License

[MIT License](LICENSE) — © 2025 Kodo Robotics
