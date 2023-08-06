from postgraas_server.management_database import init_db
import postgres_instance_driver as pg
from postgraas_server.configuration import get_config


def create_db_container():
    config = get_config()
    db_credentials = {
            "db_name": config.get('metadb', 'db_name'),
            "db_username": config.get('metadb', 'db_username'),
            "db_pwd": config.get('metadb', 'db_pwd'),
            "host": config.get('metadb', 'host'),
            "port": config.get('metadb', 'port')
        }
    try:
        db_credentials['container_id'] = pg.create_postgres_instance('postgraas_master_db', db_credentials)
    except ValueError as e:
        print "warning container already exists"
        postgraas_db = pg.get_container_by_name('postgraas_master_db')
        db_credentials['container_id'] = postgraas_db['Id']
    return db_credentials


def main():
    from postgraas_server import postgraas_api
    print "creating container for the management db"
    db_credentials = create_db_container()
    pg.wait_for_postgres(db_credentials['db_name'], db_credentials['db_username'], db_credentials['db_pwd'],
                          db_credentials['host'], db_credentials['port'])
    print "initializing db"
    init_db(db_credentials, postgraas_api.app)


if __name__ == '__main__':
    main()
