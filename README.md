# ros2em - ROS2 Environment Manager

[![PyPI version](https://img.shields.io/pypi/v/ros2em.svg)](https://pypi.org/project/ros2em/)
[![License](https://img.shields.io/github/license/Kodo-Robotics/ros2em.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-blue)](#)

**ros2em** is a CLI tool to create and manage isolated ROS2 environments.

Whether you're a robotics developer, student, or researcher, `ros2em` makes it easy to:

* 🧠 Spin up clean, persistent ROS 2 environments
* 🐳 Use Docker based containers
* 🖥 Access GUIs like Rviz or Gazebo via browser
* ✅ Support both `amd64` and `arm64` architectures

---

## 🚀 Features

* ⚡ One-line ROS 2 environment creation and access
* 🖥 Web-based GUI using [tiryoh/ros2-desktop-vnc](https://hub.docker.com/r/tiryoh/ros2-desktop-vnc)
* 🖥 GUI access using browser
* 🔐 No system pollution – nothing touches your host machine
* 💡 Powered by Typer (CLI) and Rich (colored output)

---

## 🔧 Prerequisites

Before using ros2em, make sure you have Docker installed on your system:

### 🪟 Windows
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Ensure WSL 2 is installed and configured (Docker Desktop will guide you).
3. After install, verify Docker is working `docker version`.

### 🍎 macOS
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. After installation, open Docker Desktop once to initialize.
3. After install, verify Docker is working `docker version`.

### 🐧 Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

Then test it `docker version`.

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

### 🐣 Create a new environment

```bash
ros2em init myenv --distro humble
```

Creates a `.ros2em/myenv/` folder with a default `docker-compose.yml`, metadata, and port configuration.

#### ⚙️ Options
You can customize it with advanced options.

| Option     | Type       | Default    | Description                                                                 |
|------------|------------|------------|-----------------------------------------------------------------------------|
| `--ports`  | list[str]  | None       | Extra port mappings in `host:container` format (e.g., `9000:9000`)         |
| `--context`| str        | "default"  | Docker context to use (useful for `remote` or `wsl` contexts)              |

Example:

```bash
ros2em init turtlebot4 humble --ports 11311:11311 --context wsl
```

### 🚀 Start or resume the container

```bash
ros2em up myenv
```

Starts the container if it exists, or creates it if not.

### 🧹 Stop the container

```bash
ros2em stop myenv
```

Stops the running container but **retains it**, including all manually installed packages.

### ❌ Delete an environment

```bash
ros2em delete myenv
```

Stops and removes the container. As well deletes `.ros2em/myenv/` folder and all metadata.

### 🖥 Accessing the Desktop GUI

```bash
ros2em open myenv
```

Click on the link that looks something like this in the output: `http://localhost:6080`.

---

## 🧩 Contributing

We welcome contributions, ideas, and feedback.

* [ ] Open issues for bugs and enhancements
* [ ] Fork and submit a pull request
* [ ] Share your use case via Discussions

---

## 📄 License

[Apache 2.0](LICENSE) — © 2025 Kodo Robotics
