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

from rich import print

from ros2em.backend import docker_backend
from ros2em.utils.env_utils import env_path, read_metadata

def stop_env(name: str):
    env_dir = env_path(name)
    metadata = read_metadata(env_dir)
    docker_backend.down(name, env_dir, metadata)