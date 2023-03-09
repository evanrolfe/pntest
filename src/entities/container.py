from dataclasses import dataclass


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
    host_name: str

    # Get the other containers that this one depends on
    def get_depends_on(self) -> str:
        depends_on = self.raw_container.attrs['Config']['Labels'].get('com.docker.compose.depends_on', '') # type:ignore
        return depends_on
