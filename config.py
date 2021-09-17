from utils import get_ip_address, get_total_memory


class Configuration:
    DATABASE = {
        'name': 'db.sqlite3',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False
    }
    DEBUG = True
    SECRET_KEY = ''
    # ip address
    IP_ADDRESS = get_ip_address()
    MEMORY_TOTAL = get_total_memory()
    # memory reserved for system
    MEMORY_RESERVE = 1
    SCHEDULER_API_ENABLED = True
