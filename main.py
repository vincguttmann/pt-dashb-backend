#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import json
import datetime


f = open('data.json')

data = json.load(f)
nextDepartures = []

for i in range(20):
    if data[i]["plannedDepartureTime"] / 1000 + data[i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() - 1200 >= 0:
        nextDepartures.append(data[i])

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(nextDepartures))

f.close()
