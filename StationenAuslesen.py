import csv
from urllib.request import urlopen

# import json
import json
import urllib.request, json

benoetigteStationen = ["Lueneburger Strasse", "Lerchenauer Strasse", "Curt-Mezger-Platz", "Milbertshofen", "Petuelring", "Anhalter Platz", "Olympiazentrum", "Oberwiesenfeld", "Olympiapark Eissportstadion", "Schopenhauerstrasse"]
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
                print(row[5])

# Link:https://www.mvg.de/api/fib/v1/departure?globalId=de:09162:350&limit=10&offsetInMinutes=0&transportTypes=UBAHN,BUS,SBAHN,SCHIFF

#url welche mit Slicing bearbeitet wird
url = "https://www.mvg.de/api/fib/v1/departure?globalId=-&limit=10&offsetInMinutes=0&transportTypes=UBAHN,BUS,SBAHN,SCHIFF"
for i in range(len(zwischenSpeicher)):
    usedUrl = url[:49] +zwischenSpeicher[i][5] +url[50:]
    with urllib.request.urlopen(usedUrl) as url:
        data = json.load(url)
    print(data)
    print(" ")
# Output: JSON Dateien von jeder Station die wir brauchen