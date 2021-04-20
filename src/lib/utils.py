from pendulum import Pendulum

def format_timestamp(timestamp):
    if type(timestamp) == Pendulum:
        return timestamp.format('%H:%M:%S %Y-%m-%d')
