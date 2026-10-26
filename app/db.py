import os
import oracledb

pool = None

def init_pool():
    global pool
    if pool is None:
        pool = oracledb.create_pool(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            dsn=os.environ.get("DB_DSN"),
            min=2,
            max=5,
            increment=1
        )    

def close_pool():
    global pool
    if pool is not None:
        pool.close()
        pool = None

def get_conn():
    if pool is None:
        init_pool()
    """FastAPI dependency: borrow a connection, always return it. """
    conn = pool.acquire()
    try:
        yield conn
    finally:
        pool.release(conn)