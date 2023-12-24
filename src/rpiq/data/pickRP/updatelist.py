import os
import yaml
directory = r'C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\src\rpiq\data\catagories\revamped'
titles = []

for filename in os.listdir(directory):
    if filename.endswith('.yaml'):
        title = os.path.splitext(filename)[0]
        titles.append(title)

with open('listofrps.yaml', 'w') as file:
    yaml.dump(titles, file)

print(titles)
