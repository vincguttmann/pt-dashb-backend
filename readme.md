# public transport dashboard backend
pt-dashb-backend ist das Backend zu `[Hier Frontend-Repo-Namen einfügen]`, welche zusammen ein Dashboard-System zur Anzeige von ÖPNV-Zeiten bilden.

## Datenübergabe ans Frontend
Pro Installation/Tor muss eine JSON-Datei ausgegeben werden, die über den Webserver verfügbar gemacht wird.
Die Datei folgt dem folgenden Schema:
```
[
    "stationsname1": {
        "transportTypes": ["UBAHN", "TRAM", "BUS"],
        "trips": [{
            "name": "U3",
            "type": "UBAHN",
            "plannedDeparture": 1666179240000,
            "cancelled": false,
            "delayInMinutes": 0,
            "occupancy": MEDIUM,
            "destination": "Dessauerstraße via Olympia-Einkaufszentrum U Dessauerstraße"
           },
        ],
    },
    "stationsname2": {
         "transportTypes": ["BUS"],
         "trips": [],
    },
]
```

Die anzuzeigenden Stationen werden mit dem Stationsnamen als Schlüssel aufgelistet.
In den Stationen wird angegeben, welche Verkehrstypen diese Station anfahren (`"TRAM"`, `"UBAHN"`, `"BUS"`, `"SBAHN"`), dies muss entweder fest einprogrammiert, oder aus aktuellen Stationsdaten der MVV/des MVG ausgelesen werden.

Weiterhin muss eine Liste an anstehenden Fahrten angegeben werden.

Eine Fahrt hat die folgenden Attribute:
- `name`: einfach der Linienname
- `type`: der Typ des Verkehrsmittels (`"TRAM"`, `"UBAHN"`, `"BUS"`, `"SBAHN"`)
- `plannedDeparture`: Abfahrtszeitpunkt in Unixzeit
- `cancelled`: boole`sche Angabe, ob die Fahrt abgesagt wurde
- `delayInMinutes`: Verspätung in Minuten
- `occupancy`: wie voll das Fahrzeug ist
- `destination`: Die Zielstation des Fahrzeugs

Grundsätzlich werden alle Schlüssel in camelCase/dromedarCase benannt, und die Namen sind englisch.
