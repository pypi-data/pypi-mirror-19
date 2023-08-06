__author__ = 'sebastian neubauer'
import docker
import hashlib
import psycopg2
import time


def get_unique_id(connection_dict):
    return hashlib.sha1(str(frozenset(connection_dict.items()))).hexdigest()


def get_hostname():
    #mmmh, how should this be done? need nome kind ouf routing...
    return "not imlemented yet"


def get_open_port():
    #this should be done somewhere else, e.g docker itself, but for now...
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def get_container_by_name(postgraas_instance_name):
    c = docker.Client(base_url='unix://var/run/docker.sock',
                        version='auto',
                        timeout=30)
    containers = c.containers()
    for container in containers:
        for name in container['Names']:
            if postgraas_instance_name in name.replace("/", ""):
                return container


def check_container_exists(postgraas_instance_name):
    if get_container_by_name(postgraas_instance_name):
        return True
    return False


def create_postgres_instance(postgraas_instance_name, connection_dict):
    c = docker.Client(base_url='unix://var/run/docker.sock',
                        timeout=30,
                        version='auto')
    environment = {
        "POSTGRES_USER": connection_dict['db_username'],
        "POSTGRES_PASSWORD": connection_dict['db_pwd'],
        "POSTGRES_DB": connection_dict['db_name']
    }
    internal_port = 5432
    if check_container_exists(postgraas_instance_name):
        raise ValueError('Container exists already')
    image = 'postgres:9.4'
    port_bindings = {internal_port: connection_dict['port']}
    restart_policy = {"Name": "unless-stopped"}
    host_config_dict = c.create_host_config(port_bindings=port_bindings, restart_policy=restart_policy)
    container_info = c.create_container(image,
                                        name=postgraas_instance_name,
                                        ports=[internal_port],
                                        environment=environment,
                                        labels={"postgraas": image},
                                        host_config=host_config_dict)
    container_id = container_info['Id']
    c.start(container_id)
    return container_id


def delete_postgres_instance(container_id):
    c = docker.Client(base_url='unix://var/run/docker.sock',
                        timeout=30,
                        version='auto')
    c.remove_container(container_id, force=True)
    return


def wait_for_postgres(dbname, user, password, host, port):
    for i in range(540):
        try:
            conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except psycopg2.OperationalError as e:
            print i, " ..waiting for db"
            time.sleep(1)
