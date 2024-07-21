import json

categories = [
  "35",
  "186",
  "187",
  "188",
  "189",
  "190",
  "191",
  "192",
  "193",
  "215",
  "232",
  "335",
  "338",
  "339",
  "350",
  "385",
  "389",
  "392",
  "407",
  "420",
  "422",
  "435",
]

with open("all_m3u8.json") as file:
  data = file.read()
  json_data = json.loads(data)

indian_links = []

for item in json_data:
  if item['category_id'] in categories:
    indian_links.append(item)

indian_links = [dict(t) for t in {tuple(d.items()) for d in indian_links}]

with open("indian_m3u8.json", "r+") as file:
  file.write(json.dumps(indian_links))