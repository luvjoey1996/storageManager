import random
import socket
import string
import psutil


class ServiceBuilder:

    def __init__(self):
        self.env = {}
        self.docker_params = {}
        self.service_params = {}

    def add_env(self, name, value):
        self.env[name] = value

    def add_docker_param(self, name, value):
        self.docker_params[name] = value

    def add_service_param(self, name, value):
        self.service_params[name] = value

    def settings(self):
        res = []
        for t, kv in enumerate([self.env, self.service_params, self.docker_params], start=1):
            for name, value in kv.items():
                res.append(
                    {"type_": t, "name": name, "value": value}
                )
        return res

    def set_memory(self, gb):
        self.add_docker_param("memory", "{}G".format(gb))


class RedisServiceBuilder(ServiceBuilder):

    def __init__(self):
        super().__init__()
        self.add_docker_param("--publish", ":80")

    def set_password(self, password: str):
        self.add_service_param("requirePass", password)


class MysqlServiceBuilder(ServiceBuilder):

    def set_username_and_password(self, username: str, password: str):
        self.add_env("MYSQL_USER", username)
        self.add_env("MYSQL_PASSWORD", password)


name_population = string.digits + string.ascii_letters
password_population = string.digits + string.ascii_letters + string.punctuation


def random_username():
    return random_fixed_string(name_population, 15)


def random_password():
    return random_fixed_string(password_population, 15)


def random_service_name():
    return random_fixed_string(name_population, 20)


def random_fixed_string(choices, size):
    return "".join(random.choices(choices, k=size))


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    s.close()
    return address


def get_total_memory():
    return psutil.virtual_memory().total
