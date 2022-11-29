#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import json
import datetime
import math

#testarray
input = ["olympiazentrum.json", "petuelring.json", "olympiaparkEissportstadion.json"]
def torZusammenfassung(inputFiles, outputFile, stationName):
    #inputfile: input
    #outputfile: output
    #stationname. namen der Stationen
    f = [] #zwischenspeicher
    data = [] #

    # data array wird mit inputfiles gefüllt
    for i in range(len(inputFiles)):
        with open(inputFiles[i]) as file:
            data.append(json.load(file))

    nextDeparturesStation = []
    nextDepartures = []

    # j = station
    # i = index fahrt
    # rechnet aus ob es innerhalb der nächsten 20 minuten ist
    # unwichtige Daten raushauen
    for j in range(len(data)):
        for i in range(len(data[j])):
            if data[j][i]["realtime"] is True:
                if data[j][i]["plannedDepartureTime"] / 1000 + data[j][i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() <= 1200:
                    data[j][i].pop("sev")
                    data[j][i].pop("network")
                    data[j][i].pop("stopPointGlobalId")
                    data[j][i].pop("bannerHash")
                    data[j][i].pop("messages")
                    data[j][i].pop("platform", None)
                    data[j][i].pop("realtime")
                    data[j][i].pop("trainType")
                    data[j][i]["minutesTillDeparture"] = (data[j][i]["plannedDepartureTime"] - datetime.datetime.now().timestamp()) / 1000 / 60 + data[j][i]["delayInMinutes"]
                    nextDeparturesStation.append(data[j][i])

            elif data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp() <= 1200:
                data[j][i].pop("sev")
                data[j][i].pop("network")
                data[j][i].pop("stopPointGlobalId")
                data[j][i].pop("bannerHash")
                data[j][i].pop("messages")
                data[j][i].pop("platform", None)
                data[j][i].pop("realtime")
                data[j][i].pop("trainType")
                nextDeparturesStation.append(data[j][i])
        nextDepartures.append(nextDeparturesStation.copy())
        del nextDeparturesStation[:]

    transportTypes = []
    transportTypesStation = []

    # schaut welchen Transporttyp es gibt
    # erstellt einen Array für jede Station
    for k in range(len(nextDepartures)):
        for i in range(len(nextDepartures[k])):
            double = False
            for j in range(len(transportTypesStation)):
                if nextDepartures[k][i]["transportType"] == transportTypesStation[j]:
                    double = True
            if double is False:
                transportTypesStation.append(nextDepartures[k][i]["transportType"])
        transportTypes.append(transportTypesStation.copy())
        del transportTypesStation[:]

    output = []

    # output wird erstellt
    # output ist Liste mit wichtigen Daten, die ausgegeben werden
    for i in range(len(stationName)):
        output.append({stationName[i]: {
            "transportTypes": transportTypes[i],
            "trips": nextDepartures[i]}})

    # output ausgeben in File
    with open(outputFile, "w") as outfile:
        outfile.write(json.dumps(output))

def allStations(inputFiles, outputFile, stationName):
    #inputfile: input
    #outputfile: output
    #stationname. namen der Stationen
    f = [] #zwischenspeicher
    data = []

    # data array wird mit inputfiles gefüllt
    for i in range(len(inputFiles)):
        with open(inputFiles[i]) as file:
            data.append(json.load(file))

    nextDeparturesStation = []
    nextDepartures = []

    # j = station
    # i = index fahrt
    # rechnet aus ob es innerhalb der nächsten 20 minuten ist
    # unwichtige Daten raushauen
    for j in range(len(data)):
        for i in range(len(data[j])):
            if data[j][i]["realtime"] is True:
                if data[j][i]["plannedDepartureTime"] / 1000 + data[j][i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() <= 1200 and data[j][i]["plannedDepartureTime"] / 1000 + data[j][i]["delayInMinutes"] * 60 - datetime.datetime.now().timestamp() > 0:
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

                    boo = False
                    for k in range(len(nextDeparturesStation)):
                        if nextDeparturesStation[k]["label"] == data[j][i]["label"] and nextDeparturesStation[k]["destination"] == data[j][i]["destination"]:
                            nextDeparturesStation[k]["times"].append(data[j][i]["times"][0])
                            boo = True
                    if boo is False:
                        nextDeparturesStation.append(data[j][i])

            elif data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp() <= 1200 and data[j][i]["plannedDepartureTime"] / 1000 - datetime.datetime.now().timestamp() > 0:
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

                boo = False
                for k in range(len(nextDeparturesStation)):
                    if nextDeparturesStation[k]["label"] == data[j][i]["label"] and nextDeparturesStation[k]["destination"] == data[j][i]["destination"]:
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

    # output ausgeben in File
    with open(outputFile, "w") as outfile:
        outfile.write(json.dumps(output))


allStations(input, "tor1.json", ["Olympiazentrum", "Petuelring", "Olympiapark Eissportstadion"])
