 # -*- coding: utf-8 -*-

from rasa_nlu.model import Interpreter
import pandas as pd
import numpy as np
import random 
import spacy
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

df = pd.read_csv("data/Teams_data.csv")

# generate the intents for laliga_questions intent
intents = [
'tell me something about the history of [team]',
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
            "- tell me about the city of []",
            "- tell me something about the city of [city]",
            "- do you know anything about the city of [city]?",
            "- tell me more about the city of [city]",
            "- any information about the city of [city]?"]

updated_intents_ = []
for intent in intents_:
    for team in df.Team.values.tolist():
        updated_intents_.append(intent.replace("[city]", team.replace("\n","")))

with open('intents_1.txt', 'w') as f:
    for item in updated_intents_:
        f.write("%s\n" % item)


def get_bot_response(user_message=u""):
    """Formulate the bot response given the user message
       the message must be of type unicode text 
    """

    urw_replies = [u'Happy to help you', u'You are more than Welcome!', u'No problem, Anytime!']
    nonsense_replies = [u"Sorry, I don't understand what you are saying", u"Sorry, I cannot help you on that!",\
                         u"That's not my area of expertise"]
    break_the_ice_replies = [u"Hello, Anything I can do for you?", u"Hi there! How can I help you today?"]
    friendly_replies = [u"Sure! ", u"Sure! Let's see what we have here "]

    # Findout the intent of the user's message
    interpreter = Interpreter.load("./models/current/nlu")
    message = ' '.join([x.strip() for x in user_message.split()])
    result = interpreter.parse(message)
    intent_confidence = result['intent']['confidence']
    intent_type = result['intent']['name']

    nlp = spacy.load('xx_ent_wiki_sm')
    doc = nlp(message)
    entities_txts = []
    entities_labels = []
    for ent in doc.ents:
        entities_txts.append(ent.text)
        entities_labels.append(ent.label_)
    # uncomment for debugging bot replies intents
    # print(intent_type, intent_confidence)

    if intent_confidence >= 0.5:
        if intent_type == "laliga_questions":
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG']:
                    # retrieve the history of the mentioned location/ organization in the user's message
                    history = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['History'] #df.loc[df['Team'] == txt]['History']
                    if len(history) >= 1:
                        return random.choice(friendly_replies).encode("utf-8") + history.to_string(header=False, index=False,dtype=str, max_rows=None)
                    else:
                        return random.choice(nonsense_replies).encode("utf-8")
                else:
                    return random.choice(nonsense_replies).encode("utf-8")
                     

        if intent_type == "city_questions":
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG']:
                    # retrieve an intro of the mentioned location/ organization in the user's message
                    summary = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['Summary'] #df.loc[df['Team'] == txt]['Summary']
                    if len(summary) >= 1:
                        return random.choice(friendly_replies).encode("utf-8") + summary.to_string(header=False, index=False,dtype=str, max_rows=None) 
                    else:
                        return random.choice(nonsense_replies).encode("utf-8")
                else:
                    return random.choice(nonsense_replies).encode("utf-8")

        elif intent_type == "thankyou":
            return random.choice(urw_replies).encode("utf-8")

        elif intent_type == "great":
            return random.choice(break_the_ice_replies).encode("utf-8")
        else:
            return random.choice(nonsense_replies).encode("utf-8")
    else:
        return random.choice(nonsense_replies).encode("utf-8")

             

# print(get_bot_response(u'what is the history of Real Madrid?'))
# print(get_bot_response(u'LFJLSDG DGKJSDF SKFHKDSHF KWFKHEWF LGFSGFH WELOJFWLJGLW?'))


# print(reply)
# print(txt)
# print(entities_txts)
# print(entities_labels)
# print(intent_type)

# elif intent_confidence < 0.5:


# intent = json.dumps(result, indent=2)
# print(intent)





