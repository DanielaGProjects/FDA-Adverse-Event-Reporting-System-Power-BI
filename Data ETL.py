import requests
import json

#STEP 1. Fetching data from openFDA

def fetchDataAndCreateJSON():
    # Send the GET request
    response = requests.get("https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:'corticosteroid'+AND+receivedate:[20190101+TO+20191231]&limit=5")
    myResponse = response.text

    myJson = json.loads(myResponse)

    FDA_data= myJson["results"]


    with open("drugEvents.json", "w", encoding="utf-8") as file:
        json.dump(FDA_data, file, ensure_ascii=False, indent=4)

    print("File saved!")















# Functions to call
#fetchDataAndCreateJSON()












"""1=recovered/resolved
2=recovering/resolving
3=not recovered/not
resolved
4=recovered/resolved
with sequelae
5=fatal
6=unknown"""