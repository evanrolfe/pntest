import os
from pendulum import Pendulum

def format_timestamp(timestamp):
    if type(timestamp) == Pendulum:
        return timestamp.format('%H:%M:%S %Y-%m-%d')

def is_dev_mode():
    return os.getenv('DEV_MODE') is not None
