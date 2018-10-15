 # -*- coding: utf-8 -*-

from rasa_nlu.model import Interpreter
import pandas as pd
import numpy as np
import random
import wikipedia 
import spacy
import os

pd.options.display.max_colwidth = 1000
pd.options.display.max_rows = 999
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

df = pd.read_csv("data/Teams_data.csv")

def get_bot_response(user_message=""):
    """Formulate the bot response given the user message
       the message must be of type unicode text 
    """

    urw_replies = [u'Happy to help you :)', u'You are more than Welcome! :)', u'No problem, Anytime! :)']
    nonsense_replies = [u"Sorry, I don't understand what you are saying", u"Sorry, I cannot help you on that!", u"That's not my area of expertise"]
    break_the_ice_replies = [u"Hello, Anything I can do for you?", u"Hi there! How can I help you today?"]
    friendly_replies = [u"Sure! ", u"Sure! Let's see what we have here! ", u"Yea, Sure! "]

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
    print(message)
    print(intent_type, intent_confidence)
    print(entities_txts, entities_labels)


    if intent_confidence >= 0.5:
        if intent_type == "laliga_questions":
            history = ""
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG', 'PER']:
                    # retrieve the history of the mentioned location/ organization in the user's message
                    print(txt, label)
                    history = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['History'] #df.loc[df['Team'] == txt]['History']
                    if len(history) < 1: 
                        continue
                if len(history) >= 1:
                    return random.choice(friendly_replies).encode("utf-8") + history.to_string(header=False, index=False,dtype=str, max_rows=None).replace("dtype: object","")

                return random.choice(nonsense_replies).encode("utf-8")
                # return random.choice(nonsense_replies).encode("utf-8")
                     
        elif intent_type == "city_questions":
            summary = ""
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG', 'PER']:
                    # retrieve an intro of the mentioned location/ organization in the user's message
                    print(txt, label)
                    summary = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['Summary'] #df.loc[df['Team'] == txt]['Summary']
                    if len(summary) < 1:
                        continue
                if len(summary) >= 1:
                    return random.choice(friendly_replies).encode("utf-8") + summary.to_string(header=False, index=False,dtype=str, max_rows=None).replace("dtype: object","")
                    # return random.choice(nonsense_replies).encode("utf-8")
                return random.choice(nonsense_replies).encode("utf-8")

        elif intent_type == "stadium":
            stadium = ""
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG', 'PER']:
                    # retrieve an intro of the mentioned location/ organization in the user's message
                    print(txt, label)
                    stadium = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['Stadium'] 
                    if len(stadium) < 1:
                        continue
                if len(stadium) >= 1:
                    return random.choice(friendly_replies).encode("utf-8") + stadium.to_string(header=False, index=False,dtype=str, max_rows=None).replace("dtype: object","")
                    # return random.choice(nonsense_replies).encode("utf-8")
                return random.choice(nonsense_replies).encode("utf-8")

        elif intent_type == "club_location":
            stadium_loc = ""
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG', 'PER']:
                    # retrieve an intro of the mentioned location/ organization in the user's message
                    print(txt, label)
                    stadium_loc = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['Location'] 
                    if len(stadium_loc) < 1:
                        continue
                if len(stadium_loc) >= 1:
                    return random.choice(friendly_replies).encode("utf-8") + stadium_loc.to_string(header=False, index=False,dtype=str, max_rows=None).replace("dtype: object","")
                    # return random.choice(nonsense_replies).encode("utf-8")
                return random.choice(nonsense_replies).encode("utf-8")


        elif intent_type == "stadium_capacity":
            capacity = ""
            for txt, label in zip(entities_txts, entities_labels):
                if label in ['LOC', 'ORG', 'PER']:
                    # retrieve an intro of the mentioned location/ organization in the user's message
                    print(txt, label)
                    capacity = df[(df['Team'] == txt) | (df['Team_alt'] == txt.encode("utf-8"))]['Stadiums_Capcity'] 
                    if len(capacity) < 1:
                        continue
                if len(capacity) >= 1:
                    return random.choice(friendly_replies).encode("utf-8") + capacity.to_string(header=False, index=False,dtype=str, max_rows=None).replace("dtype: int64", "")
                    # return random.choice(nonsense_replies).encode("utf-8")
                return random.choice(nonsense_replies).encode("utf-8")


        elif intent_type == "thankyou":
            return random.choice(urw_replies).encode("utf-8")

        elif intent_type == "great":
            return random.choice(break_the_ice_replies).encode("utf-8")

        return random.choice(nonsense_replies).encode("utf-8")
    else:
        return random.choice(nonsense_replies).encode("utf-8")

             
def get_bot_response_nonTexts(user_attachement):
    """
    This function replies to the user with a wikipedia image 
    to any of the cities/ clubs of his interest
    """
    x = random.choice([("Here is an image that represents the Great Club of {}".format(team), wikipedia.page(team).images[0]) for team in df.Team.values.astype(str)])
    msg, image_url = x[0], x[1]
    return msg, image_url


# print(get_bot_response(u'what is the history of Real Madrid?'))
# print(get_bot_response(u'LFJLSDG DGKJSDF SKFHKDSHF KWFKHEWF LGFSGFH WELOJFWLJGLW?'))