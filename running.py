import json
from flask import jsonify
from mdprocessor import create_json_from_markdown, create_dict_from_json
from app import dictjson
from chatutils import winCheckdata, fakehistory
# create a json file from dictjson
with open('startingWinData.json', 'w') as json_file:
    json.dump(dictjson, json_file)

with open('wincheckprompt.json', 'w') as json_file:
    json.dump(winCheckdata, json_file)
    
with open('fakehistory.json', 'w') as json_file:
    json.dump(fakehistory, json_file)
    
