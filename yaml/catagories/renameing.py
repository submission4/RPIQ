
from ruamel.yaml import YAML
import os
def rename_yaml_files_in_directory(directory):
    yaml = YAML()
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                data = yaml.load(file)

            # Extract the title
            title = data.get('title', '')

            # Rename the file
            new_file_path = os.path.join(directory, f"{title}.yaml")
            os.rename(file_path, new_file_path)

# Use the functionr
rename_yaml_files_in_directory(r"C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\catagories\Soft Skills")