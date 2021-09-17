import time

from flask import Blueprint, abort
from flask_apispec import use_kwargs, marshal_with

from config import Configuration as C
from models import Service, ServiceType, ServiceState, Setting
from serializers import ServiceCreateSchema, PaginationSchema, ServicePagingSchema, ServiceSchema
from utils import random_service_name, random_password, random_username

blueprint = Blueprint("storage", __name__, url_prefix="/api/storage")


@blueprint.route("", methods=('POST',))
@use_kwargs(ServiceCreateSchema)
def create(type, memory):
    now_in_ms = int(time.time() * 1000)
    name = random_service_name()
    password = random_password()

    param = {
        "type": type,
        "name": name,
        "username": "",
        "password": password,
        "memory": memory,
        "port": -1,
        "state": ServiceState.STARTING,
        "error_no": 0,
        "created_at": now_in_ms,
        "updated_at": now_in_ms,
    }

    if type == ServiceType.MYSQL:
        username = random_username()
        param["username"] = username

    Service.create(**param)

    return param


@blueprint.route("", methods=("GET",))
@use_kwargs(PaginationSchema, location="query")
@marshal_with(ServicePagingSchema(many=True))
def list_(page_size, current_page):
    services = Service.select(Service.name, Service.type).paginate(current_page, page_size).order_by(Service.id.desc())
    return services


@blueprint.route("/<name>", methods=["GET"])
@marshal_with(ServiceSchema)
def get(name: str):
    service = Service.get_or_none(Service.name == name)
    if service is None:
        abort(404)
    settings = Setting.select(Setting.type, Setting.name, Setting.value).where(Setting.service == service.id)
    service.settings = settings
    service.ip = C.IP_ADDRESS
    return service


@blueprint.route("/<name>/start", methods=["POST"])
def start(name: str):
    Service.update(
        state=ServiceState.STARTING
    ).where(
        Service.name == name,
        Service.state.not_in(ServiceState.STARTING, ServiceState.RUNNING)
    )
    return


@blueprint.route("/<name>/stop", methods=['POST'])
def stop(name: str):
    Service.update(
        state=ServiceState.STOPPING
    ).where(
        Service.name == name,
        Service.state.not_in(ServiceState.STOPPING, ServiceState.STOPPED)
    )
    return
