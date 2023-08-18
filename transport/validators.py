import re
from datetime import datetime
from itertools import cycle


def plate(data):
    if re.match("[A-Z]{2}[0-9]{4}|[B-DF-HJ-NP-TV-Z]{4}[0-9]{2}", data.upper()):
        return True
    else:
        return False


def year(data):
    return 1990 <= data <= datetime.now().year + 1


def ci(data):
    data = data.replace(".", "")

    if "-" not in data:
        return False

    n, dv = data.split("-")

    s = 0
    for x, y in zip(n[::-1], cycle(range(2, 8))):
        s += int(x) * y

    m = 11 - s % 11
    if m == 11:
        m = "0"
    elif m == 10:
        m = "K"
    else:
        m = str(m)

    return dv == m
