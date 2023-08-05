from streampy import Stream
from streamcollector import Collector
import threading
import os

peoples = [
    {'name': 'Camille', 'age': 24},
    {'name': 'Laurent', 'age': 22},
    {'name': 'Matthias', 'age': 21},
    {'name': 'Bertrand', 'age': 25},
    {'name': 'David', 'age': 22},
    ]

res = {
    21: 1,
    22: 2,
    24: 1,
    25: 1
    }

lst = Stream(peoples) \
    .collect(Collector.count_by(lambda x: x['name']))
print lst
