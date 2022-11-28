from datetime import datetime

# Daten der Pendelbusse mit Linie, LinienID, Ziel, Zwischenhalten und Station mit deren Start und Abfahrtzeiten
Pendelbus = {
    "DF1": {
        "stations": {
            "Riesenfeldstraße": {
                "start": "Riesenfeldstraße",
                "times": ["07:42", "08:22", "09:02", "09:42", "10:22", "11:02", "11:42", "12:22", "13:02", "13:42",
                          "14:22", "15:02", "15:42", "16:22", "17:02", "17:20"]
            }},
        "route": "Dostlerstraße - Freimann",
        "id": 1,
        "destination": "Freimann",
        "stopover": "ITZ/FIZ"
    },
    "DT2": {
        "stations": {
            "Dostlerstraße": {
                "start": "Dostlerstraße",
                "times": ["08:00", "08:40", "09:20", "10:00", "10:40", "11:20", "12:00", "12:40", "13:20", "14:00",
                          "14:40", "15:20", "16:00", "16:40"]
            }},
        "route": "Dostlerstraße - Taunusstraße",
        "id": 2,
        "destination": "Taunusstraße",
        "stopover": "ITZ/FIZ"
    }
}


# Daten der Werksbusse mit Schicht, Zeit und Station
# Werksbus = {
#     "Frühschicht": {
#         "Dostlerstraße": {
#             "station": "Dostlerstraße",
#             "time": "15:15"
#         },
#         "Riesenfeldstraße": {
#             "station": "Riesenfeldstraße",
#             "time": "15:15"
#         }
#     },
#     "Spätschicht": {
#         "Dostlerstraße": {
#             "start": "Dostlerstraße",
#             "time": "00:20"
#         },
#         "Riesenfeldstraße": {
#             "start": "Riesenfeldstraße",
#             "time": "00:20"
#         }
#     },
#     "Nachtschicht": {
#         "Dostlerstraße": {
#             "start": "Dostlerstraße",
#             "time": "06:10"
#         },
#         "Riesenfeldstraße": {
#             "start": "Riesenfeldstraße",
#             "time": "06:10"
#         }
#     },
#     "Normalschicht": {
#         "Dostlerstraße": {
#             "start": "Dostlerstraße",
#             "time": "15:35"
#         },
#         "Riesenfeldstraße": {
#             "start": "Riesenfeldstraße",
#             "time": "15:35"
#         }
#     }
# }


# Sucht alle Abfahrten in den nächten 3h raus
# übergeben werden die Route(Format: %Start%Destination%ID) und die Station
def getNextBus(thisStation):
    now = datetime.now()
    nextBus = []
    for route in Pendelbus:
        for station in Pendelbus[route]["stations"]:
            for time in Pendelbus[route]["stations"][station]["times"]:
                hourBus = datetime.strptime(time, '%H:%M').hour
                minBus = datetime.strptime(time, '%H:%M').minute
                # Zeit bis zur Abfahrt berechnen
                minDiff = ((hourBus - now.hour) * 60) + minBus - now.minute

                if hourBus == 17 and minBus == 20 and 0 < minDiff < 18:
                    cache = {
                        "typ": "Pendelbus",
                        "route": 'Dostlerstraße - FIZ/Projekthaus[3]',
                        "id": 2,
                        "destination": 'FIZ/Projekthaus[3]',
                        "stopover": 'ITZ',
                        "departure": minDiff
                    }
                    nextBus.append(cache)

                elif 0 < minDiff <= 180 and station == thisStation:
                    cache = {
                        "typ": "Pendelbus",
                        "route": Pendelbus[route]["route"],
                        "id": Pendelbus[route]["id"],
                        "destination": Pendelbus[route]["destination"],
                        "stopover": Pendelbus[route]["stopover"],
                        "departure": minDiff
                    }
                    nextBus.append(cache)

    # for shift in Werksbus:
    #     for station in Werksbus[shift]:
    #         hourBus = datetime.strptime(Werksbus[shift][station]["time"], '%H:%M').hour
    #         minBus = datetime.strptime(Werksbus[shift][station]["time"], '%H:%M').minute
    #
    #         # Zeit bis zur Abfahrt berechnen
    #         minDiff = ((hourBus - now.hour) * 60) + minBus - now.minute
    #
    #         if 0 < minDiff <= 180:
    #             cache = {
    #                 "typ": "Werksbus",
    #                 "route": "",
    #                 "id": 0,
    #                 "destination": "",
    #                 "stopover": "",
    #                 "departure": minDiff
    #             }
    #             nextBus.append(cache)

    nextBus = sorted(nextBus, key=lambda d: d['departure'])

    return nextBus