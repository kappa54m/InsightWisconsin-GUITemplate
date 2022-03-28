import os
from io import StringIO
from typing import List
import csv


def list_to_csv(lst: List[str], strip=True, **kw):
    with StringIO() as sio:
        writer = csv.writer(sio, quoting=kw.get('quoting', csv.QUOTE_MINIMAL))
        writer.writerow(lst)
        ret = sio.getvalue()
    if strip:
        ret = ret.strip()
    return ret


def csv_to_list(s: str):
    if not s:
        return []
    with StringIO(s) as sio:
        reader = csv.reader(sio)
        return next(reader)
