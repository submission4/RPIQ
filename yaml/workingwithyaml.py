import yaml

# Load YAML from a file
with open(r'C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\fakehistorry.yaml', 'r') as file:
    data = yaml.safe_load(file)
from pprint import pprint as pp
pp(data)
# Access YAML data
pp(data.keys())
pp(data.items())

pp(data['history'])
pp(data['history'][0])
pp(data['win_conditions'])

# Load YAML from a string
yaml_string = """
---
title: YAML Example
""" 
data = yaml.safe_load(yaml_string)
# Access YAML data
pp("\n\n\n")
print(data['title'])
