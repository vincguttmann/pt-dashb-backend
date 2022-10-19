# import urllib library
from urllib.request import urlopen

# import json
import json
import urllib.request, json

with urllib.request.urlopen("https://www.mvg.de/api/fib/v1/departure?globalId=de:09162:351&limit=10&offsetInMinutes=0&transportTypes=UBAHN,BUS,SBAHN,SCHIFF") as url:
    data = json.load(url)
    print(data)