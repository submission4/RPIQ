import os
import frontmatter
gamedata = {}
def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        post = frontmatter.load(file)
    return post

def extract_title(post):
    return post.get('title')

def extract_roles(post):
    return post.get('roles')

def extract_win_conditions(post):
    return post.get('win_conditions')

def extract_metadata(post):
    title = extract_title(post)
    roles = extract_roles(post)
    objectives = post.get('objectives')
    win_conditions = extract_win_conditions(post)
    scenario = post.content
    return title, roles, objectives, win_conditions, scenario

def get_titles_from_folder(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    titles = [os.path.splitext(file)[0] for file in files]
    return titles

def gamedatadict(title, roles, objectives, win_conditions, scenario):
    gamedata['title'] = title
    gamedata['roles'] = roles
    gamedata['objectives'] = objectives
    gamedata['win_condition_1'] = win_conditions[0]
    gamedata['win_condition_2'] = win_conditions[1]
    gamedata['scenario'] = scenario
    return gamedata
def select_title(title):
    post = read_markdown_file(os.path.join(r'C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown', f"{title}.md"))
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    return title, roles, objectives, win_conditions, scenario

def listofrolls(roles):
    r1,r2 = roles.split(",")
    return r1,r2

def select_role(role):
    gamedata['role'] = role
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
    files = [f for f in os.listdir(r'C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown' + "\\" + catagory) if f.endswith('.md')]
    titles = [os.path.splitext(file)[0] for file in files]
    return titles
print(get_catagorys_from_folder(r'C:\Users\submi\OneDrive\Documents\pythonProjects\roleplayApp\markdown'))
print(get_titles_from_catagory("Soft Skills"))
