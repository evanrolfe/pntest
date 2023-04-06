from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
# A Docker container
class Container():
    id: str
    short_id: str
    name: str
    status: str
    ports: dict[str,list[dict]]
    image: str
    networks: list[str]
    raw_container: object
    host_name: str
    ip: str
    # The original gateway IP addr that this container was started with
    gateway: str
    interception_active: bool = False

    def __post_init__(self):
        self.interception_active = self.has_tools_installed()

    # Get the other containers that this one depends on
    def get_depends_on(self) -> str:
        depends_on = self.raw_container.attrs['Config']['Labels'].get('com.docker.compose.depends_on', '') # type:ignore
        return depends_on

    def human_readable_desc(self) -> str:
        desc = f'ID: {self.id}\n'
        desc += f'Name: {self.name}\n'
        desc += f'Image: {self.image}\n'
        desc += f'Host Name: {self.host_name}\n'
        desc += f'Status: {self.status}\n'
        desc += f'Ports: {self.ports}\n'
        desc += f'Network(s): {self.networks}'

        return desc

    # Check if ip and curl are installed on the container
    def has_tools_installed(self) -> bool:
        _, output = self.raw_container.exec_run("ip help") # type:ignore
        has_ip = 'usage' in output.decode().lower()

        _, output = self.raw_container.exec_run("curl --help") # type:ignore
        has_curl = 'usage' in output.decode().lower()

        return has_ip and has_curl

    def set_gateway(self, gateway_container: Container):
        cmd = "ip route del default"
        self.__run_cmd(cmd, privileged=True)

        cmd = f"ip route add default via {gateway_container.ip} dev eth0"
        self.__run_cmd(cmd, privileged=True)

        # The table 200 rule is necessary for container2container traffic
        cmd = f"ip rule add from {self.ip} table 200"
        self.__run_cmd(cmd, privileged=True)

        cmd = f"ip route add default via {gateway_container.ip} table 200"
        self.__run_cmd(cmd, privileged=True)

    def reset_gateway(self):
        cmd = "ip route del default"
        self.__run_cmd(cmd, privileged=True)

        cmd = f"ip route add default via {self.gateway} dev eth0"
        self.__run_cmd(cmd, privileged=True)

        cmd = f"ip route show table 200"
        self.__run_cmd(cmd, privileged=True)

    def __run_cmd(self, cmd: str, privileged=False):
        code, output = self.raw_container.exec_run(cmd, privileged=privileged) # type:ignore
        print("Command: ", cmd, "\nCode: ", code, " Output: ", output)
