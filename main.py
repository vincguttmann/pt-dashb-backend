#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import json


f = open('data.json')

data = json.load(f)
nextDepartures = []

for i in range(5):
    nextDepartures.append(data[i])

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(nextDepartures))

f.close()
