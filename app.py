import os
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, send
from chatutils import checkWinCondition, get_ai_message, winCheckdata
from mdprocessor import (
    backup_session,
    create_dict_from_json,
    extract_metadata,
    get_catagorys_from_folder,
    get_titles_from_catagory,
    read_fakehistory,
    read_markdown_file,
    read_start_wincheck,
    read_wincheck_current,
    read_wincheck_prompt,
    save_currentrp_data,
)
import json
from settings.ignoredsettings import OPENAIAPIKEY
from openai import api_key


###############################
# app setup#
# api key set enviro ##
dictjson = {
    "EvaluationTask": "Evaluate user interaction based on 'The Negotiation Challenge'",
    "Metrics": {
        "Relevance": {
            "Score": 5,
            "Feedback": "The user demonstrated a keen focus on the task by directly addressing the purchasing interest which is highly relevant to the negotiation scenario.",
        },
        "Clarity": {
            "Score": 4,
            "Feedback": "The user's intentions are clear, they are interested in buying a new computer. However, specifics regarding the requirements were not provided in the initial inquiry.",
        },
        "Completeness": {
            "Score": 3,
            "Feedback": "The user initiated the buying process but did not provide enough detail on what they are looking for in a new computer setup which is necessary for reaching a complete understanding.",
        },
        "Logic": {
            "Score": 5,
            "Feedback": "The user logically approached the conversation by showing interest and asking for the price, which is an appropriate first step in a negotiation about a purchase.",
        },
        "Creativity": {
            "Score": 2,
            "Feedback": "The user's approach was straightforward and lacked negotiation tactics that could foster creativity, such as proposing a starting price or specific conditions.",
        },
        "Engagement": {
            "Score": 5,
            "Feedback": "The user was engaged in the interaction, initiating the conversation with a friendly greeting and direct interest in the computer setup.",
        },
        "Politeness": {
            "Score": 5,
            "Feedback": "The user maintained a polite tone throughout the interaction which is conducive to a positive negotiation.",
        },
        "Adaptability": {
            "Score": 4,
            "Feedback": "The user reacted to the AI's request for more information adaptively, but this would be clearer with further interaction.",
        },
        "Language": {
            "Score": 5,
            "Feedback": "The language used was appropriate for the context of a negotiation, friendly and business-like.",
        },
        "Effectiveness": {
            "Score": 4,
            "Feedback": "The user's approach was effective in starting the negotiation, but there's room for improvement in strategy to optimize for desired outcomes.",
        },
    },
    "AnalysisOfWinConditions": "The user has begun the negotiation process effectively by expressing interest, setting a favorable foundation for future interactions.",
    "WinAssessment": {
        "Winner": "--- TBD ---",
        "ReasonForWin": "The negotiation is in its early stages and the winner cannot be determined until further interactions unfold and final terms are discussed and agreed upon.",
        "PercentageMetrics": {
            "Role1": ["Buyer", "98%"],
            "Role2": ["seller", "55%"],
        },
    },
}
# #check that open ai apy is set and working# #
listofkeys = list(dictjson["Metrics"].keys())
print(listofkeys)


class GameSession:
    def __init__(self):
        self.gameinfo = {}
        self.history = []
        self.win_check = {}

    def wincheckscores(self):
        self.win_check["Relevance"] = "none"
        self.win_check["Clarity"] = "none"
        self.win_check["Completeness"] = "none"
        self.win_check["Creativity"] = "none"
        self.win_check["Logic"] = "none"
        self.win_check["Engagement"] = "none"
        self.win_check["Politeness"] = "none"
        self.win_check["Adaptability"] = "none"
        self.win_check["Language"] = "none"
        self.win_check["Effectiveness"] = "none"
        self.win_check["AnalysisOfWinConditions"] = "none"
        self.win_check["WinAssessment"] = "none"
        self.win_check["Effectiveness"] = "none"

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
        self.gameinfo["category"] = "category"
        self.gameinfo["title"] = "title"
        self.gameinfo["roles"] = "roles"
        self.gameinfo["objectives"] = "objectives"
        self.gameinfo["win_conditions"] = "win_conditions"
        self.gameinfo["scenario"] = "scenario"
        self.gameinfo["win_check"] = "un-scored"
        return self.gameinfo

    def get_gameinfo(self):
        return self.gameinfo

    def get_history(self):
        return self.history

    def get_win_info(self):
        return self.gameinfo["win_check"]


from openai import api_key

print(api_key)
# # ## ##

# ##
##
#############################3#
# Index page
app = Flask(__name__, static_url_path="/static")  # Make sure to include this line
markdown_path = os.path.join(app.root_path, "markdown")
app.config["SECRET_KEY"] = "secret_key"
socketio = SocketIO(app)
session = GameSession()
session.build_gameinfo()
gameinfo = session.get_gameinfo()
print("gameinfo \n", gameinfo)
print("session \n", session)
history = session.get_history()
print("history \n", history)


# Index page
@app.route("/")
def index():
    categories = get_catagorys_from_folder(markdown_path)
    return render_template("index.html", categories=categories)


# Roleplay selection page
@app.route("/roleplay_selection/<category>", methods=["GET"])
def roleplay_selection(category):
    titles = get_titles_from_catagory(category)
    return render_template("roleplay_selection.html", category=category, titles=titles)


# Role selection page
@app.route("/role_selection/<category>/<title>", methods=["GET"])
def role_selection(category, title):
    post = read_markdown_file(os.path.join(markdown_path, f"{category}\\{title}.md")) 
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    gameinfo["category"] = category
    gameinfo["title"] = title
    gameinfo["roles"] = roles
    gameinfo["objectives0"] = objectives[0]
    gameinfo["objectives1"] = objectives[1]
    gameinfo["win_condition0"] = win_conditions[0]
    gameinfo["win_condition1"] = win_conditions[1]
    gameinfo["scenario"] = scenario
    print("gameinfo", gameinfo)
    
    return render_template("role.html", category=category, title=title, roles=roles)


# Chat page
@app.route("/chat", methods=["POST", "GET"])
def chat():
    global gameinfo, history , session
    user_role = request.form["user_role"]
    ai_role = request.form["ai_role"]
    session.gameinfo["user_role"] = user_role
    session.gameinfo["ai_role"] = ai_role
    print("session", session.gameinfo["user_role"])
    print("session", session.gameinfo["ai_role"])   
    session.history.append(session.gameinfo)
    
    session.win_check = read_fakehistory()
    session.gameinfo["win_check"] = session.win_check

    post = read_markdown_file(
        os.path.join(markdown_path, f"{gameinfo['category']}\\{gameinfo['title']}.md")
    )
    gameinfo = save_currentrp_data(gameinfo)
    dj = create_dict_from_json(gameinfo)
    print(type(dj))
    
    wincheckprompt = read_wincheck_prompt()
    wincheck = read_start_wincheck()
    title, roles, objectives, win_conditions, scenario = extract_metadata(post)
    print("gameinfo['user_role']", gameinfo["user_role"])
    print("gameinfo['ai_role']", gameinfo["ai_role"])
    session.gameinfo["title"] = title
    session.gameinfo["objectives"] = objectives[1]
    session.gameinfo["objectives"] = objectives[0]
    session.gameinfo["scenario"] = scenario
    session.gameinfo["win_condition0"] = win_conditions[0]
    session.gameinfo["win_condition1"] = win_conditions[1]
    session.gameinfo["win_check"] = wincheck
    session.gameinfo["wincheckprompt"] = wincheckprompt
    session.gameinfo["roles"] = roles
    session.gameinfo["history"] = history
    session.gameinfo["user_role"] = user_role
    session.gameinfo["ai_role"] = ai_role
    # Append the gameinfo to the history
    session.history.append(gameinfo)
    session.win_check = dictjson
    session.gameinfo["win_check"] = read_wincheck_current()
    print("session", session)
    session = backup_session(session)
    # Render the chat template with the metadata
    return render_template(
        "chat.html", gameinfo=gameinfo, session=session
    )  # SocketIO events



def send_data(event, data, sender):
    emit(event, {"sender": sender, "message": data})


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("message")
def handle_message(data):
    global gameinfo, history
    # parse data to dict
    print("data", data)

    if gameinfo == {}:
        print("gameinfo is empty")
        gameinfo["gameinfo"] = "empty"
        print(gameinfo)
    if gameinfo == None:
        gameinfo = {}
        gameinfo["gameinfo"] = "empty"
        print(gameinfo)

    message = data
    history.append("user: " + str(message))
    res = get_ai_message(message, history=history)
    history.append("ai: " + res)
    print(len(history))
    send_data("message", res, "Ai")
    print(res)


@socketio.on("win_check")
def win_check(data):
    global session
    sc = session.wincheckscores()
    print("sc", sc)
    r = checkWinCondition(
        history=str(history),
        win1=gameinfo["win_conditions"][0],
        win2=gameinfo["win_conditions"][1],
    )
    session.gameinfo["win_check"] = r
    last_check = session.get_win_info()
    print("____________________________________")
    print("last check type", type(last_check))
    print("last check", last_check)
    # create json / dict object from str, must remove ' from str and json from start
    last_check = last_check.replace("'", "")
    last_check = last_check.replace("json", "")
    js = json.loads(str(last_check))

    session.win_check = js
    send_data("win_check", json.dumps(js), "win_check")
    print("js")


if __name__ == "__main__":
    socketio.run(app, debug=True)
