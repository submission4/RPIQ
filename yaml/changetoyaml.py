import os

def rename_files_in_dir(directory):
    for filename in os.listdir(directory):
        base_file, ext = os.path.splitext(filename)
        if ext != ".yaml":
            os.rename(
                os.path.join(directory, filename),
                os.path.join(directory, f"{base_file}.yaml")
            )

# Use the function
rename_files_in_dir(r"C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\catagories\Beginning Test RPs")
import yaml
import os

def transform_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Transform the data to match the structure of the selected YAML
    transformed_data = {
        'catagory': data.get('catagory', 'Beginning Test RPs'),
        'title': data.get('title', ''),
        'roles': data.get('roles', {}),
        'objectives': data.get('objectives', {}),
        'win_conditions': data.get('win_conditions', {}),
        'scenario': data.get('scenario', []),
        'game_data': data.get('game_data', None),
        'win_check': data.get('win_check', None),
    }

    with open(file_path, 'w') as file:
        yaml.safe_dump(transformed_data, file)

# Use the function
directory = "/path/to/your/directory"
for filename in os.listdir(directory):
    if filename.endswith(".yaml"):
        transform_yaml_file(os.path.join(directory, filename))