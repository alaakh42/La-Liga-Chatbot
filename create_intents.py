import pandas as pd

df = pd.read_csv("data/Teams_data.csv")

# # generate the intents for laliga_questions intent
intents = ['tell me something about the history of [team]',
        'Can you tell me the history of [team]',
        "do you know anything about [team]'s history",
        "any info about [team]'s history",
        "any information about [team]'s history",
        'talk me through the history of [team] ',
        'state the short history of [team]',
        'what is the story of [team]?',
        "tell me more about [team]'s histroy",
        "tell me about [team]'s past",
        "tell me about the beginning of the [team] team",
        "how [team] was started?",
        "tell me about the foundation of the [team] team"]

intents_ = ["- what do you know about the city of [city]?",
            "- can you tell me more about the city of [city]?",
            "- tell me about the city of [city]",
            "- tell me something about the city of [city]",
            "- do you know anything about the city of [city]?",
            "- tell me more about the city of [city]",
            "- any information about the city of [city]?"]

intents1 = ["What is the name of [team]'s stadium?",
            "What is the [team] team stadium called?",
            "What is [team] stadium called?",
            "Can you tell me what is the name of [team] stadium?",
            "Can you tell me the name of [team] stadium?"]

intents2 = ["What is the capcity of [team]'s stadium?",
            "What is the capcity of [team] team stadium?",
            "How many people can the [team] team stadium take?",
            "Can you tell me what is the capcity of [team]'s stadium?",
            "Can you tell me how many people the [team] stadium could take?"]

intents3 = ["What is the location of [team]'s stadium?",
            "What is the location of [team] team stadium called?",
            "Where is the [team] stadium located?",
            "Can you tell me what is the location of [team] team stadium?",
            "Can you tell me where is the [team] stadium?"]

updated_intents_ = []
updated_intents_1 = []
updated_intents_2 = []
updated_intents_3 = []
updated_intents_4 = []
for intent, intent_ , intent__ , intent1, intent2 in zip(intents1, intents2, intents3, intents, intents_):
    for team in df.Team.values.tolist():
        updated_intents_.append(intent.replace("[team]", team.replace("\n","")))
        updated_intents_1.append(intent_.replace("[team]", team.replace("\n","")))
        updated_intents_2.append(intent__.replace("[team]", team.replace("\n","")))
        updated_intents_3.append(intent1.replace("[team]", team.replace("\n","")))
        updated_intents_4.append(intent2.replace("[city]", team.replace("\n","")))

with open('intents.txt', 'w') as f:
    for item in updated_intents_:
        f.write( '- ' + "%s\n" % item)
    for item1 in updated_intents_1:
        f.write( '- ' + "%s\n" % item1)
    for item2 in updated_intents_2:
        f.write( '- ' + "%s\n" % item2)
    for item3 in updated_intents_3:
        f.write( '- ' + "%s\n" % item3)
    for item4 in updated_intents_4:
        f.write( '- ' + "%s\n" % item4)


