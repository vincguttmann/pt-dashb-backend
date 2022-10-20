import json
import datetime


f = open('data.json')

data = json.load(f)
nextDepartures = []

for i in range(20):
    if data[i]["plannedDepartureTime"] / 1000 + data[i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() - 1200 >= 0:
        data[i].pop("sev")
        data[i].pop("network")
        data[i].pop("stopPointGlobalId")
        data[i].pop("bannerHash")
        data[i].pop("messages")
        data[i].pop("platform", None)
        data[i].pop("realtime")
        data[i].pop("trainType")
        nextDepartures.append(data[i])

dictionary1 = {"Olympiazentrum": {
    "transportTypes": ["UBAHN", "BUS"],
               "trips": nextDepartures}}

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(dictionary1))

f.close()
