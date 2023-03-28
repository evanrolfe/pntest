from dataclasses import dataclass


@dataclass(kw_only=True)
# A Docker network
class Network():
    id: str
    name: str
    scope: str
    driver: str
    labels: dict[str, str]
    raw_network: object
    subnet: str
    gateway: str

    def container_ids(self) -> list[str]:
        return list(self.raw_network.attrs['Containers'].keys()) # type: ignore

    def human_readable_desc(self) -> str:
        desc = f'ID: {self.id}\n'
        desc += f'Name: {self.name}\n'
        desc += f'Driver: {self.driver}\n'
        desc += f'Subnet: {self.subnet}\n'
        desc += f'Labels: {self.labels}'

        return desc
