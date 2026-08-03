import requests
import json
import re
import Dictionaries

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






#STEP 2. Adding MedDRA definitions to JSON Files
def MedDRA_definitions():
    for var_name, variable_value in vars(Dictionaries).items():
        
        # Filtering internal variables (starting with '__')
        if not var_name.startswith("__"):
                pattern = r"(\d+)=(.*?)(?=\n\d+=|\Z)"

                coincidences = re.findall(pattern, variable_value)

                dict = {myKey: val for myKey, val in coincidences}

                with open("./MedDRA_definitions/"+ var_name +".json", "w", encoding="utf-8") as file:
                    json.dump(dict, file, ensure_ascii=False, indent=4)













# Functions to call
#fetchDataAndCreateJSON()
MedDRA_definitions()







def fromStringToJson():
    text = """1=recovered/resolved
    2=recovering/resolving
    3=not recovered/not resolved
    4=recovered/resolved with sequelae
    5=fatal
    6=unknown"""

    pattern = r"(\d+)=(.*?)(?=\n\d+=|\Z)"


    coincidences = re.findall(pattern, text)


    dict = {myKey: val for myKey, val in coincidences}

    reactionoutcome = json.dumps(dict, indent=2)

    print(reactionoutcome)