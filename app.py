import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
from chatutils import checkWinCondition, get_ai_message
from mdprocessor import extract_metadata, get_catagorys_from_folder, get_titles_from_catagory, get_titles_from_folder, read_markdown_file
import json
from settings.ignoredsettings import OPENAIAPIKEY
from openai import api_key
###############################
#app setup#
#api key set enviro ##
# #check that open ai apy is set and working# #

class GameSession:
    def __init__(self):
        self.gameinfo = {}
        self.history = []
        self.last_check = ""
    
    def __getitem__(self, key):
        return self.gameinfo[key]
    
    def __setitem__(self, key, value):
        self.gameinfo[key] = value
    
    def __str__(self):
        return str(self.gameinfo)
    
    def __repr__(self):
        return str(self.gameinfo)
    
    def __len__(self):
        return len(self.gameinfo)
    
    def __iter__(self):
        return iter(self.gameinfo)
    
    def __next__(self):
        return next(self.gameinfo)
    
    def __delitem__(self, key):
        del self.gameinfo[key]
        
    def __contains__(self, key):
        return key in self.gameinfo
    
    def build_gameinfo(self):
        self.gameinfo['category'] = "category"
        self.gameinfo['title'] = "title"
        self.gameinfo['roles'] = "roles"
        self.gameinfo['objectives'] = "objectives"
        self.gameinfo['win_conditions'] = "win_conditions"
        self.gameinfo['scenario'] = "scenario"
        return self.gameinfo
    def get_gameinfo(self):
        return self.gameinfo
    
    def get_history(self):
        return self.history
    
    def get_last_check(self):
        return self.last_check
    
from openai import api_key
print(api_key)
# # ## ##

# ##
##
#############################3#
# Index page
app = Flask(__name__, static_url_path='/static')  # Make sure to include this line
markdown_path = os.path.join(app.root_path, 'markdown')
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)
session = GameSession()
session.build_gameinfo()
gameinfo = session.get_gameinfo()
print("gameinfo \n" ,gameinfo)
print("session \n" ,session)
history = session.get_history()
print("history \n", history)
# Index page
@app.route('/')
def index():
    categories = get_catagorys_from_folder(markdown_path)
    return render_template('index.html', categories=categories)

# Roleplay selection page
@app.route('/roleplay_selection/<category>', methods=['GET'])
def roleplay_selection(category):
    titles = get_titles_from_catagory(category)
    return render_template('roleplay_selection.html', category=category, titles=titles)

# Role selection page
@app.route('/role_selection/<category>/<title>', methods=['GET'])
def role_selection(category, title):
    post = read_markdown_file(os.path.join(markdown_path, f"{category}\\{title}.md"))
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    gameinfo['category'] = category
    gameinfo['title'] = title
    gameinfo['roles'] = roles
    gameinfo['objectives'] = objectives
    gameinfo['win_conditions'] = win_conditions
    gameinfo['scenario'] = scenario
    print("gameinfo",gameinfo)
    return render_template('role.html', category=category, title=title, roles=roles)

# Chat page
@app.route('/chat', methods=['POST'])
def chat():
    global gameinfo, history
    # Extract the user role from the request form and save it to gameinfo
    role = request.form['role'].strip("}'':{").replace("'", "").replace(":", "")
    gameinfo['user_role'] = role
    # Find and save the ai role to gameinfo
    print("roles",gameinfo['roles'])
    print("role",role)
    gameinfo['ai_role'] = next(i for i in gameinfo['roles'] if i != role)
    print("ai role",gameinfo['ai_role'])
    # Read the markdown file for the selected category and title
    post = read_markdown_file(os.path.join(markdown_path, f"{gameinfo['category']}\\{gameinfo['title']}.md"))
    # Extract the metadata from the post
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    # Append the gameinfo to the history
    session.history.append(gameinfo)
    # Render the chat template with the metadata
    return render_template('chat.html', gameinfo=gameinfo)# SocketIO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')

def handle_message(data):
    global gameinfo , history
    # parse data to dict
    print("data",data )
    print("_____________________________")
    # print("user role",gameinfo['user_role'])
    # print("ai role",gameinfo['ai_role'])
    # print("roles",gameinfo['roles'])
    # print("role",gameinfo['role'])
    import pprint
    if gameinfo == {}:
        print("gameinfo is empty")
        gameinfo['gameinfo'] = "empty"
        print(gameinfo)
    elif gameinfo == None:
        gameinfo = {}
        gameinfo['gameinfo'] = "empty"
        print(gameinfo)
    pprint.pprint(gameinfo)
    print("_____________________________")


    if 'message' not in data.keys():
        print("no message")
        return
    print(data)
    message = data['message']
    history.append("user: " + message)
    res = get_ai_message(message, history=history)
    history.append("ai: " + res)
    print(len(history))
    send({'message': res}, broadcast=True)
@socketio.on('win_check')
def win_check(data):
    print("from wincheck",data)
    r = checkWinCondition(history =str(history),win1 = gameinfo['win_conditions'][0],win2 = gameinfo['win_conditions'][1])
    last_check = r

    lc = last_check.split("```")
    lc1 = lc[1].replace(";", "\n<br>")
    lc1 = lc1.replace("java Map scores = new HashMap<>()", " ")
    lc1 = lc1.replace('scores.put("', " ")
    lc1 = lc1.replace('"', " ")
    lc1 = lc1.replace(")", " ")
    print("___________________",lc1,"_________________")
    send({"win_check":lc1})
    print("last check",last_check)
if __name__ == '__main__':
    socketio.run(app, debug=True)
