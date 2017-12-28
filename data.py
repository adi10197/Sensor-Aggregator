import random
import sched
import time
import json

data = []

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    data.append({
        'time': time.time(),
        'sensor1': random.uniform(0, 1),
        'sensor2': random.uniform(0, 1),
        'sensor3': random.uniform(0, 1),
        'sensor4': random.uniform(0, 1),
        'sensor5': random.uniform(0, 1),
        'sensor6': random.uniform(0, 1),
        'sensor7': random.uniform(0, 1),
        'sensor8': random.uniform(0, 1)
    })
    s.enter(1, 1, do_something, (sc,))
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

s.enter(1, 1, do_something, (s,))
s.run()
