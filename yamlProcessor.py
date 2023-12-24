import datetime
import yaml

class YamlProcessor:
    def __init__(self, catagory, title):
        self.catagory = catagory
        self.title = title
        self.file_path = self.create_file_path()

    def create_file_path(self):
        file_path = r'C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml' + "\\" + self.catagory + "\\" + self.title + ".yaml"
        return file_path

    def open_yaml(self):
        with open(self.file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data

    def save_yaml(self, data):
        with open(self.file_path, 'w') as file:
            yaml.dump(data, file)

    def update_yaml(self, key, value):
        yaml_data = self.open_yaml()
        yaml_data[key] = value
        self.save_yaml(yaml_data)

    def create_yaml(self, data):
        required_keys = ['title', 'category', 'role-one', 'role-two', 'objectives', 'win_conditions']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        self.save_yaml(data)

    def get_history(self):
        yaml_data = self.open_yaml()
        return yaml_data.get('history', [])

    def update_ui(self):
        # Code to update the UI goes here
        pass
    
    def save_game_history(self, gamedata):
        filePathForSaves = r"C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\saves"
        savedFileName= self.title + datetime.datetime.now() +".yaml"
        with open(filePathForSaves + savedFileName, 'w') as file:
            yaml.dump(gamedata, file)
        return "Complete"
    
    @staticmethod
    def list_catagories():
        import os
        catagorys = [f for f in os.listdir(r'C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\catagories', )] 
        return catagorys
    
    @staticmethod
    def list_titles(catagory):
        import os
        files = [f for f in os.listdir(r'C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\yaml\catagories\\' +   catagory)]
        print(files)
        return files

yaml_processor = YamlProcessor.list_catagories()
print(yaml_processor)
print("")
print(yaml_processor[1])
title = YamlProcessor.list_titles(yaml_processor[1])
print(title)
# Example usage:
# catagory = "example_category"
# title = "example_title"
# yaml_processor = YamlProcessor(catagory, title)
# yaml_processor.update_yaml("key", "value")
