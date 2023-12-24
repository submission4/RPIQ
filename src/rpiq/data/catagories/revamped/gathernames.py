import os  
listfile = []

def gather_names(directory):
    # open the directory
    directory = os.listdir(directory)
    for each in directory:
        print(each)
        if each.endswith(".yaml"):
            each = each.replace(".yaml", "")
            listfile.append(each)
    return listfile

listfile = gather_names(r"C:\Users\submi\OneDrive\Documents\pythonProjects\rpiq\RPIQ\src\rpiq\data\catagories\revamped")
print(listfile) 

