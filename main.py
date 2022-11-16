#imports
import json
import datetime

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


torZusammenfassung(input, "tor1.json", ["Olympiazentrum", "Petuelring", "Olympiapark Eissportstadion"])
