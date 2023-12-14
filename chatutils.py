from openai import OpenAI
import os
from settings.ignoredsettings import OPENAIAPIKEY

print("openaikey", OPENAIAPIKEY)
os.environ["OPENAI_API_KEY"] = OPENAIAPIKEY
apicheck = os.environ["OPENAI_API_KEY"]
client = OpenAI()
print(client.api_key)
# set the api key
client.api_key = os.environ["OPENAI_API_KEY"]
print(client.api_key)
print(apicheck)
print(OPENAIAPIKEY)
print(os.environ["OPENAI_API_KEY"])
print(client.models.list)


def checkAPIexsits():
    try:
        if api_key == None:
            print("api key not set")

        elif apicheck == None:
            print("api key not set")

        print("api key exists")
        return

    except Exception or apicheck == None or api_key == None:
        print("api key needs to be set")
        print(str(Exception))


checkAPIexsits()


def get_ai_message(user_input, history):
    # take the prompt and generate the next text
    print("history", history)
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "MAKE SURE TO ALWAYS STAY IN CHARACTER and only respond as your role"
                + str(history)
                + "PLEASE START INTERACTION GIVING YOUR ROLE AND GREET THE OTHER PERSON if youve already greeted them dont do it twice",
            },
            {"role": "user", "content": str(user_input)},
        ],
    )

    respon = completion.choices[0].message.content
    return respon


def checkWinCondition(history, win1, win2):
    # take the prompt and generate the next text
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "Evaluate the user interaction and determine the winner"
                + """
            {
            "EvaluationTask": "Evaluate user interaction",
            "Metrics": {
                "Relevance": "Rate how the interaction aligns with the original prompt (1-5)",
                "Clarity": "Assess the clarity of the user's instructions or questions (1-5)",
                "Completeness": "Evaluate if all necessary details are provided (1-5)",
                "Logic": "Gauge the logic behind the user's statements (1-5)",
                "Creativity": "Rate the user's creativity and exploration (1-5)",
                "Engagement": "Assess user engagement with model responses (1-5)",
                "Politeness": "Evaluate the politeness and tone of the interaction (1-5)",
                "Adaptability": "Determine adaptability to model's outputs (1-5)",
                "Language": "Check appropriateness of the language used (1-5)",
                "Effectiveness": "Give an overall effectiveness rating (1-5)",
                        },
                    "AnalysisOfWinConditions": "Review user's interaction history to assess win conditions",
                    "WinAssessment": {
                        "Winner": "Name or description of the winner, if applicable",
                        "ReasonForWin": "Explanation of what led to the win",
                        "PercentageMetrics": {
                            "Role1": "Percentage success rate for Role 1",
                            "Role2": "Percentage success rate for Role 2",
                            "AdditionalRoles": "Percentage success rates for any additional roles",
                        },
                    },
                    "ResponseFormat": "Provide scores and brief feedback for each metric, determine the winner, and explain the reason for the win with percentage metrics for each role",
                },""",
            },
            {"role": "user", "content": str(history)},
        ],
    )
    # completion = client.chat.completions.create(
    #         model="gpt-4-1106-preview",
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": [],
    #             },
    #             {
    #                 "role": "user",
    #                 "content": str(history)
    #                 }],
    #             )
    r = completion.choice
    print("r", r)
    respon = completion.choices[0].message.content
    print("respon", respon)
    return respon
