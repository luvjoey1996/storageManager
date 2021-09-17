from peewee import *

from app import db


class ServiceState:
    STARTING = 1
    RUNNING = 2
    STOPPING = 3
    STOPPED = 4
    ERROR = 5
    RESOURCE_UNAVAILABLE = 6

    @classmethod
    def as_choices(cls):
        return (ServiceState.STARTING, ServiceState.RUNNING, ServiceState.STOPPING,
                ServiceState.STOPPED, ServiceState.ERROR, ServiceState.RESOURCE_UNAVAILABLE)


class ServiceType:
    REDIS = 1
    MYSQL = 2

    @classmethod
    def as_choices(cls):
        return ServiceType.REDIS, ServiceType.MYSQL


class SettingType:
    ENV = 1
    COMMAND_LINE = 2
    DOCKER = 3

    @classmethod
    def as_choices(cls):
        return SettingType.ENV, SettingType.COMMAND_LINE, SettingType.DOCKER


class Service(db.Model):
    type = SmallIntegerField(null=False, choices=ServiceType.as_choices(), help_text="1: redis, 2: mysql")
    name = CharField(null=False, max_length=20, unique=True, help_text="name of this service")

    username = CharField(null=False, max_length=10, help_text="username used to connect this service")
    password = CharField(null=False, max_length=15, help_text="password used to connect this service")
    port = SmallIntegerField(null=False, default=-1, help_text="port number of this service")
    memory = SmallIntegerField(null=False, default=1, help_text="memory required for this service (GB)")
    state = SmallIntegerField(null=False, choices=ServiceState.as_choices(),
                              help_text='1: starting, 2: running, 3: stopping, 4: stopped, 5: error')
    error_no = SmallIntegerField(null=False, default=0, help_text="error code of docker container")

    created_at = BigIntegerField(null=False)
    updated_at = BigIntegerField(null=False)


class Setting(db.Model):
    service = IntegerField(null=False, index=True)

    type = SmallIntegerField(null=False, choices=SettingType.as_choices(),
                             help_text="1: environment variable, 2: command line , 3: docker")
    name = CharField(null=False, max_length=30, help_text="name of this setting")
    value = CharField(null=False, max_length=30, help_text="value of this setting")
