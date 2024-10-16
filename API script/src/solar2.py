

# https://192.168.0.201/data/l10n/en-US.json has strings for each nubmber
# https://192.168.0.201/data/ObjectMetadata_Istl.json has string numbers for each measurment

import requests

server = "192.168.0.201"

strings_url = "https://192.168.0.201/data/l10n/en-US.json"
metadata_url = "https://192.168.0.201/data/ObjectMetadata_Istl.json"

strings_json = requests.get(url=strings_url, verify=False)
metadata_json = requests.get(url=metadata_url, verify=False)

strings = strings_json.json()
metadata = metadata_json.json()

def num_to_str(num):
    return strings[str(num)]

def metadata_format(key):
        data = metadata[key]
        try:
            name = num_to_str(data["TagId"])
        except:
            name = data["TagId"]
        try:
            unit = num_to_str(data["Unit"])
        except:
            unit = "?"
        return f"{key}: {name} ({unit})\n"

file = open("test.txt", "w")

for key in list(metadata.keys()):
    file.write(metadata_format(key))

file.close()

