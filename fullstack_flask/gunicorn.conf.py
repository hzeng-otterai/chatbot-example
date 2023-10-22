import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv()

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = "0.0.0.0:50505"

if os.getenv("RUNNING_IN_PRODUCTION"):
    workers = (multiprocessing.cpu_count() * 2) + 1
    threads = workers
else:
    reload = True
    workers = 2
    threads = 2

timeout = 120
