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


    with open("./JSONFiles/drugEvents.json", "w", encoding="utf-8") as file:
        json.dump(FDA_data, file, ensure_ascii=False, indent=4)

    print("File saved!")



def manipulatingData():
    with open('./JSONFiles/drugEvents.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    #To avoid unnested tables and simplify them, the content was split in 3 different tables, using safetyreportid as a foreign key
    main_reports = []
    drugs_list = []
    reactions_list = []

    keys_to_remove = {"package_ndc", "spl_id", "spl_set_id", "product_ndc", "nui"}

    for d in data:
        report_id = d.get("safetyreportid")
        
        # 1. Extracting reactions and adding safetyreportid to create a fact table
        patient = d.get("patient", {})
        reactions = patient.get("reaction", [])
        
        for r in reactions:
            # a new dictionary is created, safetyreportid is added
            reaction_entry = {"safetyreportid": report_id}
            reaction_entry.update(r)  # adding the rest of the reactions dictionary
            reactions_list.append(reaction_entry)

        # 2. A new dictionary is created, safetyreportid is added
        drugs = patient.get("drug", [])
        for drug in drugs:
            drug_entry = {"safetyreportid": report_id}
            drug_copy = drug.copy()
            
            # filtering unnecessary keys
            if "openfda" in drug_copy and isinstance(drug_copy["openfda"], dict):
                drug_copy["openfda"] = {
                    k: v for k, v in drug_copy["openfda"].items() 
                    if k not in keys_to_remove
                }
                
            drug_entry.update(drug_copy)
            drugs_list.append(drug_entry)

        # 3. Creating a main fact table (without reactions and drugs)
        report_copy = d.copy()
        if "patient" in report_copy:
            # Removing 
            report_copy["patient"] = {
                k: v for k, v in report_copy["patient"].items() 
                if k not in ["drug", "reaction"]
            }
        main_reports.append(report_copy)

    with open('./JSONFiles/fact_safety_reports.json', 'w', encoding='utf-8') as f:
        json.dump(main_reports, f, indent=4)

    with open('./JSONFiles/fact_report_reactions.json', 'w', encoding='utf-8') as f:
        json.dump(reactions_list, f, indent=4)

    with open('./JSONFiles/fact_report_drugs.json', 'w', encoding='utf-8') as f:
        json.dump(drugs_list, f, indent=4)

    print("Files created")




#STEP 2. Adding MedDRA definitions to JSON Files
def MedDRA_definitions():
    for var_name, variable_value in vars(Dictionaries).items():
        
        # Filtering internal variables (starting with '__')
        if not var_name.startswith("__"):
                pattern = r"(\d+)=(.*?)(?=\n\d+=|\Z)"

                coincidences = re.findall(pattern, variable_value)

                dict = {myKey: val for myKey, val in coincidences}

                json_data = {var_name: dict}

                with open("./MedDRA_definitions/"+ var_name +".json", "w", encoding="utf-8") as file:
                    json.dump(json_data, file, ensure_ascii=False, indent=4)













# Functions to call
#fetchDataAndCreateJSON()
#MedDRA_definitions()
manipulatingData()


