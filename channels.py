import json


with open("m3u8.json") as file:
  data = file.read()
  json_data = json.loads(data)

for item in json_data:
  print(item)