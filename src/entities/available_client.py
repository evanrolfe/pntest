from dataclasses import dataclass
import platform
import re
import subprocess
from typing import Optional

# AvailableClient is a client that is available to be started on the machine that this code is running on.
# Unlike other models it does not represent a row in the database.
@dataclass(kw_only=True)
class AvailableClient():
    name: str
    commands: list[str]
    command: Optional[str]
    version: Optional[str]
    regex: str
    type: str

    def enabled(self):
        if self.name == 'anything':
            return True

        return (self.command is not None)

    # Run through each of the commands and if any of them work, then set the command to that value
    def verify_command(self):
        result = None
        for command in self.commands:
            result = self.__check_command(command)
            if result is not None:
                self.command = command
                break

        if result is None:
            return

        output = result.stdout.decode().strip()
        matches = re.match(self.regex, output)

        if matches:
            self.version = matches[1]

    def __check_command(self, command: str):
        pltfrm = platform.system()

        if pltfrm == "Windows":
            raise Exception("starting browsers not yet implemented on windows!")
        elif pltfrm == "Darwin":
            return self.__check_command_unix(command)
        else:
            return self.__check_command_unix(command)

    def __check_command_unix(self, command: str):
        try:
            result = subprocess.run([command, '--version'], stdout=subprocess.PIPE)
            return result
        except FileNotFoundError:
            return None
