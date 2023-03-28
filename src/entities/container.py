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
