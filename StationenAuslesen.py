import csv
from urllib.request import urlopen
import json
import datetime
import math

benoetigteStationen = ["Curt-Mezger-Platz", "Anhalter Platz", "Lueneburger Strasse", "Petuelring", "Olympiazentrum", "Milbertshofen"]
zwischenSpeicher = []

#CSV Datei öffnen
with open('MVV_Stationen_2.csv') as csvdatei:
    #fieldnames = ['HstNummer','Name mit Ort','Name ohne Ort','Ort','GKZ','Globale ID','MVTT X','MVTT Y','WGS84 X','WGS84 Y']
    csv_reader_object = csv.reader(csvdatei)

    #für jede Zeile schauen ob eine Station, welche wir brauchen, drinnen steht
    for row in csv_reader_object:
        for i in benoetigteStationen:
            if(i == row[1]):
                zwischenSpeicher.append(row)

# Link:https://www.mvg.de/api/fib/v1/departure?globalId=de:09162:350&limit=10&offsetInMinutes=0&transportTypes=UBAHN,BUS,SBAHN,SCHIFF

#url welche mit Slicing bearbeitet wird
url = "https://www.mvg.de/api/fib/v1/departure?globalId=-&limit=10&offsetInMinutes=0&transportTypes=UBAHN,BUS,SBAHN,SCHIFF"
data = []

for i in range(len(zwischenSpeicher)):
    usedUrl = url[:49] +zwischenSpeicher[i][5] +url[50:]
    # store the response of URL
    response = urlopen(usedUrl)

    # storing the JSON response
    # from url in data
    data.append(json.loads(response.read()))

for i in range(len(data)):
    with open(benoetigteStationen[i] + ".json", "w") as outfile:
        outfile.write(json.dumps(data[i]))

# Output: JSON Dateien von jeder Station die wir brauchen

# Daten der Pendelbusse mit Linie, LinienID, Ziel, Zwischenhalten und Station mit deren Start und Abfahrtzeiten
Pendelbus = {
    "DF1": {
        "stations": {
            "Dostlerstraße": {
                "start": "Dostlerstraße",
                "times": ["07:40", "08:20", "09:00", "09:40", "10:20", "11:00", "11:40", "12:20", "13:00", "13:40",
                          "14:20", "15:00", "15:40", "16:20", "17:00"]
            },
            "Riesenfeldstraße": {
                "start": "Riesenfeldstraße",
                "times": ["07:42", "08:22", "09:02", "09:42", "10:22", "11:02", "11:42", "12:22", "13:02", "13:42",
                          "14:22", "15:02", "15:42", "16:22", "17:02"]
            }},
        "route": "Dostlerstraße - Freimann ",
        "id": 1,
        "destination": "Freimann",
        "stopover": "ITZ/FIZ"
    },
    "DT2": {
        "stations": {
            "Dostlerstraße": {
                "start": "Dostlerstraße",
                "times": ["08:00", "08:40", "09:20", "10:00", "10:40", "11:20", "12:00", "12:40", "13:20", "14:00",
                          "14:40", "15:20", "16:00", "16:40", "17:20"]
            }},
        "route": "Dostlerstraße - Taunusstraße",
        "id": 2,
        "destination": "Taunusstraße",
        "stopover": "ITZ/FIZ"
    }
}

def allStations(inputFiles, outputFile, stationName):
    #inputfile: input
    #outputfile: output
    #stationname. namen der Stationen
    f = [] #zwischenspeicher
    data = []

    # data array wird mit inputfiles gefüllt
    for i in range(len(inputFiles)):
        with open(inputFiles[i], encoding='utf8') as file:
            data.append(json.load(file))

    nextDeparturesStation = []
    nextDepartures = []

    # j = station
    # i = index fahrt
    # rechnet aus ob es innerhalb der nächsten 30 Minuten ist
    # unwichtige Daten raushauen
    for j in range(len(data)):
        for i in range(len(data[j])):
            if data[j][i]["realtime"] is True:
                if data[j][i]["plannedDepartureTime"] / 1000 + data[j][i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() <= 1800 and data[j][i]["plannedDepartureTime"] / 1000 + data[j][i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() > 0 and data[j][i]["cancelled"] is False:
                    data[j][i].pop("sev")
                    data[j][i].pop("network")
                    data[j][i].pop("stopPointGlobalId")
                    data[j][i].pop("bannerHash")
                    data[j][i].pop("messages")
                    data[j][i].pop("platform", None)
                    data[j][i].pop("realtime")
                    data[j][i].pop("trainType")
                    data[j][i].pop("occupancy")
                    data[j][i]["times"] = [{"minutesTillDeparture": math.ceil((data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp()) / 60 + data[j][i]["delayInMinutes"]), "onTime": True, "cancelled": data[j][i].pop("cancelled")}]
                    if data[j][i]["delayInMinutes"] > 0:
                        data[j][i]["times"][0]["onTime"] = False
                    if "Expressbus" in data[j][i]["destination"]:
                        data[j][i]["destination"] = data[j][i]["destination"].split("Expressbus ")[1]
                    if " via" in data[j][i]["destination"]:
                        data[j][i]["destination"] = data[j][i]["destination"].split(" via")[0]
                    if "Bf." in data[j][i]["destination"]:
                        data[j][i]["destination"] = data[j][i]["destination"].split("Bf.")[0] + 'Bf.'

                    boo = False
                    for k in range(len(nextDeparturesStation)):
                        if nextDeparturesStation[k]["label"] == data[j][i]["label"] and nextDeparturesStation[k]["destination"] == data[j][i]["destination"]:
                            if len(nextDeparturesStation[k]["times"]) < 3:
                                nextDeparturesStation[k]["times"].append(data[j][i]["times"][0])
                            boo = True
                    if boo is False:
                        nextDeparturesStation.append(data[j][i])

            elif data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp() <= 1800 and data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp() > 0 and data[j][i]["cancelled"] is False:
                data[j][i].pop("sev")
                data[j][i].pop("network")
                data[j][i].pop("stopPointGlobalId")
                data[j][i].pop("bannerHash")
                data[j][i].pop("messages")
                data[j][i].pop("platform", None)
                data[j][i].pop("realtime")
                data[j][i].pop("trainType")
                data[j][i].pop("occupancy")
                data[j][i]["times"] = [{"minutesTillDeparture": math.ceil((data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp()) / 60), "onTime": True, "cancelled": data[j][i].pop("cancelled")}]
                if "Expressbus" in data[j][i]["destination"]:
                    data[j][i]["destination"] = data[j][i]["destination"].split("Expressbus ")[1]
                if " via" in data[j][i]["destination"]:
                    data[j][i]["destination"] = data[j][i]["destination"].split(" via")[0]
                if "Bf." in data[j][i]["destination"]:
                    data[j][i]["destination"] = data[j][i]["destination"].split("Bf.")[0] + 'Bf.'

                boo = False
                for k in range(len(nextDeparturesStation)):
                    if nextDeparturesStation[k]["label"] == data[j][i]["label"] and nextDeparturesStation[k]["destination"] == data[j][i]["destination"]:
                        if len(nextDeparturesStation[k]["times"]) < 3:
                            nextDeparturesStation[k]["times"].append(data[j][i]["times"][0])
                        boo = True
                if boo is False:
                    nextDeparturesStation.append(data[j][i])
        nextDepartures.append(nextDeparturesStation.copy())
        del nextDeparturesStation[:]

    output = {"entries": len(stationName), "stations": {}}

    # output wird erstellt
    # output ist Liste mit wichtigen Daten, die ausgegeben werden
    for i in range(len(stationName)):
        output["stations"][stationName[i]] = nextDepartures[i]

    output["stations"]["Pendelbusse"] = getNextBus()
    output["entries"] += 1

    # output ausgeben in File
    with open(outputFile, "w", encoding='utf8') as outfile:
        outfile.write(json.dumps(output, ensure_ascii=False))


# Sucht alle Abfahrten in den nächten 3h raus
# übergeben werden die Route(Format: %Start%Destination%ID) und die Station
def getNextBus():
    thisStation = "Dostlerstraße"
    now = datetime.datetime.now()
    dic1 = {"destination": "Freimann",
            "transportType": "bmwbus",
            "times": []}
    dic2 = {"destination": "Taunusstraße",
            "transportType": "bmwbus",
            "times": []}
    dic3 = {"destination": "FIZ/Projekthaus[3]",
            "transportType": "bmwbus",
            "times": []}
    nextBus = [dic1, dic2, dic3]

    for route in Pendelbus:
        for station in Pendelbus[route]["stations"]:
            for time in Pendelbus[route]["stations"][station]["times"]:
                hourBus = datetime.datetime.strptime(time, '%H:%M').hour
                minBus = datetime.datetime.strptime(time, '%H:%M').minute

                # Zeit bis zur Abfahrt berechnen
                minDiff = ((hourBus - now.hour) * 60) + minBus - now.minute

                if hourBus == 17 and minBus == 20 and 0 < minDiff < 18:
                    cache = {
                        #"route": 'Dostlerstraße - FIZ/Projekthaus[3]',
                        #"id": 2,
                        "destination": 'FIZ/Projekthaus[3]',
                        #"stopover": 'ITZ',
                        "minutesTillDeparture": minDiff,
                        "onTime": True
                    }
                    if cache["destination"] == "Freimann":
                        nextBus[0]['times'].append(cache)
                    elif cache["destination"] == "Taunusstraße":
                        nextBus[1]['times'].append(cache)
                    elif cache["destination"] == "FIZ/Projekthaus[3]":
                        nextBus[2]['times'].append(cache)

                elif 0 < minDiff <= 40 and station == thisStation:
                    cache = {
                        #"transportType": "bmwbus",
                        #"route": Pendelbus[route]["route"],
                        #"id": Pendelbus[route]["id"],
                        "destination": Pendelbus[route]["destination"],
                        #"stopover": Pendelbus[route]["stopover"],
                        "minutesTillDeparture": minDiff,
                        "onTime": True
                    }
                    if cache["destination"] == "Freimann":
                        nextBus[0]['times'].append(cache)
                    elif cache["destination"] == "Taunusstraße":
                        nextBus[1]['times'].append(cache)
                    elif cache["destination"] == "FIZ/Projekthaus[3]":
                        nextBus[2]['times'].append(cache)


    #nextBus = sorted(nextBus, key=lambda d: d['departure'])
    for i in range(len(nextBus)):
        for j in range(len(nextBus[i]['times'])):
            nextBus[i]['times'][j].pop("destination")
        if len(nextBus[i]['times']) == 0:
            nextBus.remove(nextBus[i])
    return nextBus



allStations(["Anhalter Platz.json", "Curt-Mezger-Platz.json","Milbertshofen.json","Lueneburger Strasse.json", "Olympiazentrum.json", "Petuelring.json"], "/var/www/html/yeet.json", ["Anhalter Platz", "Curt-Mezger-Platz","Milbertshofen","Lüneburger Straße", "Olympiazentrum", "Petuelring"])