#import json


# Opening JSON file
f = open('data.json')

# returns JSON object as
# a dictionary
data = json.load(f)


print data

# Closing file
f.close()
