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
