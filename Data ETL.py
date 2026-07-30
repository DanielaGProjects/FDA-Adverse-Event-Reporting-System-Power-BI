import requests
import json

baseURL = "https://api.fda.gov/drug/event.json"

# Send the GET request

response = requests.get("https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:'corticosteroid'&limit=5")

myResponse = response.text

myJson = json.loads(myResponse)

FDA_data= myJson["results"]


with open("drugEvents.json", "w", encoding="utf-8") as file:
    json.dump(FDA_data, file, ensure_ascii=False, indent=4)

print("File saved!")