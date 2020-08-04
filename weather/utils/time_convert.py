import datetime


def to_time(minutes: int):
    return datetime.time(hour=minutes // 60, minute=minutes % 60)


def to_int(time_: datetime.time):
    return time_.hour * 60 + time_.minute
