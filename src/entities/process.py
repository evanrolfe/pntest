from dataclasses import dataclass
from dataclasses import field
import platform
import re
import subprocess
from typing import Optional

@dataclass(kw_only=True)
class Process():
    proc: subprocess.Popen
    type: str
