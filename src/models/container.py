from dataclasses import dataclass
from dataclasses import field
import platform
import re
import subprocess
from typing import Optional
import docker

@dataclass(kw_only=True)

# A Docker container
class Container():
    short_id: str
    name: str
    status: str
    ports: dict[str,list[dict]]
    image: str
    networks: list[str]
    raw_container: object
