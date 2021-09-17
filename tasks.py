import podman
import podman.errors
from peewee import fn

from app import scheduler
from config import Configuration as C
from models import Service, ServiceState, ServiceType

docker_client = podman.from_env()


@scheduler.task("interval", id="status_sync", seconds=3)
def status_sync():

    services = Service.select().where(Service.state == ServiceState.STOPPING)
    for service in services:
        try:
            container = docker_client.containers.get(service.name)
            if container.status.lower() == 'exited':
                service.update(state=ServiceState.STOPPED)
            else:
                container.stop()
        except podman.errors.NotFound:
            pass
    available_memory = C.MEMORY_TOTAL - C.MEMORY_RESERVE
    used_memory = Service.select(fn.SUM(Service.memory)).where(Service.state == ServiceState.RUNNING)
    available_memory -= used_memory

    services = Service.select().where(Service.state == ServiceState.STARTING)
    for service in services:
        try:
            container = docker_client.containers.get(service.name)
            status = container.status.lower()

            if status == 'running':
                port = int(container.ports.keys()[0].split("/")[0])
                service.update(state=ServiceState.RUNNING, port=port)
                service.save()
            elif status == "exited":
                if available_memory > service.memory:
                    container.restart()
                    available_memory -= service.memory

        except podman.errors.NotFound:
            service2image = {
                ServiceType.MYSQL: "mysql",
                ServiceType.REDIS: "redis"
            }
            service2port = {
                ServiceType.MYSQL: ":3306",
                ServiceType.REDIS: ":6379"
            }
            used_memory -= service.memory
            if used_memory > 0:
                docker_client.containers.run(
                    service2image[service.type],
                    ports={"": service2port[service.type]},
                    mem_limit="%sG" % service.memory
                )
            else:
                used_memory += service.memory
