# app/services/db_pool.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from urllib.parse import quote_plus

from utils.db_pool import DbConnectionPool
from utils.db_client import DbClient



db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "rest"
}
db_pool = DbConnectionPool(db_config)
db_client = DbClient(db_pool)

sd = db_client.query("SELECT * FROM prompt_cache")
print(sd)