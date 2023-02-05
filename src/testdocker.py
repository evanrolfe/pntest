import docker
from repos.container_repo import ContainerRepo
from services.client_service import ClientService

def attach_to_container(container_ids: list[str]):
    client = docker.from_env()
    containers = client.containers.list()

    # ID of the example-backend container:

    # for container in containers:
    #     print(container.short_id)
    #     print(container.name)
    #     print(container.image.tags)
    #     print(container.status)
    #     print(container.ports)
    # return

    # 1. Find the container to intercept and stop it
    try:
        container = [c for c in containers if c.short_id == id][0]
    except IndexError:
        return

    image = container.attrs['Config']['Image'] # type:ignore
    # network_mode = container.attrs['HostConfig']['NetworkMode'] # type:ignore
    networks = list(container.attrs['NetworkSettings']['Networks'].keys()) # type:ignore
    network = networks[0]

    if len(networks) > 1:
        raise Exception("The docker container must only be on a single network")

    print(f'Stopping container: {container.short_id}')
    container.stop() # type:ignore
    print('Stopped.')

    # 2. Start the proxy container
    proxy_image = 'pntest-proxy:latest'
    print(f'Starting container with image: {proxy_image}')
    proxy_env = ['CLIENT_ID=2', 'ZMQ_SERVER=host.docker.internal:5556']
    proxy_container = client.containers.run(
        proxy_image,
        detach=True,
        privileged=True,
        environment=proxy_env,
        ports=container.ports,  #type:ignore
        network=network
    )
    print(f'started proxy container: {proxy_container.short_id}') # type:ignore

    # 3. Start a container to intercept but using the proxy container's network
    print(f'Starting container with image: {image}')
    client.containers.run(image, detach=True, network=f'container:{proxy_container.short_id}') # type:ignore
    print('Done.')

id = '831aa94f4700'
# attach_to_container([id])

print("starting...")
container_repo = ContainerRepo.get_instance()
client_service = ClientService.get_instance()
container = container_repo.find_by_short_id(id)
if container is None:
    raise Exception("no container found with id ", id)

print("found container: ", container.raw_container)
# container_repo.proxify_container(container)
client = client_service.build_client('docker', container)
print("client before: ", client)
client_service.launch_client(client)

print("client after: ", client)
