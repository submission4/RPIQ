import datetime
import json
import os
import frontmatter
import pandas as pd

pd.set_option("display.max_colwidth", None)
gamedata = {}


# use pandas to read read json file

def load_json_as_dict(filename):
    # Read the JSON file into a DataFrame
    df = pd.read_json(filename)

    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict()

    return data_dict
rr = load_json_as_dict("json/static/fakehistory.json")

(print(rr))


def read_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        post = frontmatter.load(file)
    return post


def extract_title(post):
    return post.get("title")


def extract_roles(post):
    return post.get("roles")


def extract_win_conditions(post):
    return post.get("win_conditions")


def extract_metadata(post):
    title = extract_title(post)
    roles = extract_roles(post)
    objectives = post.get("objectives")
    win_conditions = extract_win_conditions(post)
    scenario = post.content
    return title, roles, objectives, win_conditions, scenario


def get_titles_from_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
    titles = [os.path.splitext(file)[0] for file in files]
    return titles


def gamedatadict(title, roles, objectives, win_conditions, scenario):
    gamedata["title"] = title
    gamedata["roles"] = roles
    gamedata["objectives"] = objectives
    gamedata["win_condition_1"] = win_conditions[0]
    gamedata["win_condition_2"] = win_conditions[1]
    gamedata["scenario"] = scenario
    return gamedata


def select_title(title):
    post = read_markdown_file(
        os.path.join(
            r"C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown",
            f"{title}.md",
        )
    )
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    return title, roles, objectives, win_conditions, scenario


def listofrolls(roles):
    r1, r2 = roles.split(",")
    return r1, r2


def select_role(role):
    gamedata["role"] = role
    return gamedata


def makeprompt(gamedata):
    prompt = f"{gamedata['title']}\n\n{gamedata['scenario']}\n\n{gamedata['objectives']}\n\n{gamedata['win_condition_1']}\n\n{gamedata['win_condition_2']}"
    return prompt


# get catagorys from folder names
def get_catagorys_from_folder(folder_path):
    catagorys = [f for f in os.listdir(folder_path)]
    return catagorys


# get titles from catagory selected folder
def get_titles_from_catagory(catagory):
    files = [
        f
        for f in os.listdir(
            r"C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown"
            + "\\"
            + catagory
        )
        if f.endswith(".md")
    ]
    titles = [os.path.splitext(file)[0] for file in files]
    return titles


print(
    get_catagorys_from_folder(
        r"C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown"
    )
)
print(get_titles_from_catagory("Soft Skills"))

# make the current app rp into a json file


def save_currentrp_data(gamedata):
    import json

    with open("json/currentapprp.json", "w") as json_file:
        json.dump(gamedata, json_file)
    return json_file


def save_to_prevous(gamedata):
    import json

    with open("json/previousrp.json", "w") as json_file:
        json.dump(gamedata, json_file)
    return json_file


def read_previous():
    import json

    with open("json/previousrp.json") as json_file:
        data = json.load(json_file)
    return data


def save_wincheck(wincheck):
    import json

    with open("json/wincheckprompt.json", "w") as json_file:
        json.dump(wincheck, json_file)
    return json_file


def read_wincheck_prompt():
    import json

    with open("json/static/wincheckprompt.json") as json_file:
        data = json.load(json_file)
    print(type(data))
    data = str(data)
    return data


def read_wincheck_current():
    import json

    with open("json/currentwincheck.json") as json_file:
        data = json.load(json_file)
    return data


def backup_session(session):
    import json

    with open("json/session.json", "w") as json_file:
        json.dump(session, json_file)
    return json_file


def read_current():
    import json

    with open("currentapprp.json") as json_file:
        data = json.load(json_file)
    return data


def read_fakehistory():
    import json

    with open("json/static/fakehistory.json") as json_file:
        data = json.load(json_file)
    return data


def read_start_wincheck():
    import json

    with open("json\static\startingWinData.json") as json_file:
        data = json.load(json_file)
    return data


def save_history():
    import json

    durrp = read_current()
    jsonfilke = durrp
    print(durrp)
    with open(f"json\saves\history{datetime.datetime.now()}.json") as json_file:
        json.dump(jsonfilke, json_file)
    return json_file


def read_json():
    import json

    with open("gamedata.json") as json_file:
        data = json.load(json_file)
    return data


def update_json(gamedata, key, value):
    import json

    # insure that the gamedata id a dict
    if type(gamedata) != dict:
        # if not convert it to a dict from a json file
        gamedata = read_json(gamedata)
        gamedata = gamedata.to_dict()
    # update the dict with the key and value
    if key is not None:
        gamedata[key] = value
    # save the dict as a json file
    with open("gamedata.json", "w") as json_file:
        json.dump(gamedata, json_file)
    # convert to usable dict
    gamedata = read_json()
    return gamedata


def get_json_value(gamedata, key):
    import json

    # insure that the gamedata id a dict
    if type(gamedata) != dict:
        # if not convert it to a dict from a json file
        gamedata = read_json(gamedata)
        gamedata = json.load(gamedata)
    # get the value from the key
    value = gamedata[key]
    return value


# create a dict from a json file for use in the app
def create_dict_from_json(json_file):
    import json

    with open(json_file) as json_file:
        data = json.load(json_file)
    if data is not dict:
        data = data.to_dict()
        return data
    else:
        return data


# create json file from the metadata of a markdown file
def create_json_from_markdown(markdown_file):
    import json

    post = read_markdown_file(markdown_file)
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    gamedata = gamedatadict(title, roles, objectives, win_conditions, scenario)
    with open("gamedata.json", "w") as json_file:
        json.dump(gamedata, json_file)
    return json_file
