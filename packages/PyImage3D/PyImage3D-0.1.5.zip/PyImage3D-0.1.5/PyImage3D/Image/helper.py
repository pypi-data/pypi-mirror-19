import uuid
from datetime import datetime


def to_timestamp(dt=datetime.now(), epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def unique_id():
    return str(uuid.uuid4())
