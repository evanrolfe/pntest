from dataclasses import dataclass
import subprocess

@dataclass(kw_only=True)
class Process():
    proc: subprocess.Popen
    type: str
