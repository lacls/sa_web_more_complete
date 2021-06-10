
from rq import Connection, Worker
from main_folder import conn, queue
if __name__ == "__main__":
    with Connection(conn):
        w = Worker([queue],default_worker_ttl=60 * 60 * 24 * 7)
        w.work()
