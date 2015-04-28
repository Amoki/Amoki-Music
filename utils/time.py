import isodate


def get_time_in_seconds(time):
    return isodate.parse_duration(time).total_seconds()
