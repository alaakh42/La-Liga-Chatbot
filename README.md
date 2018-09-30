# La Liga Clubs History Chatbot

This repo is an attemt to solve the Clubs history challenge!

This chatbot can have a comprehensive conversation with the user while giving him/ her some information about the history of La Liga Clubs

## UPDATE
It seems that the App is Live and public but not yet verified by facebook whcih, means that no one can use it but Admin and Testers, I will work on this now

### Install Requirements

To install the project dependencies, run the following command
	`sudo -H pip install -r requirements.txt`


## Getting Started

1. Run Flask Server `python app.py`, remember to change `app.run(port=8888, debug=True)` to your port number

2. Run ngrok `ngrok http 8888`
	- optionally you can open ngrok web interface `http://127.0.0.1:4042/inspect/http` to keep an eye on the `GET` and `POST` requests


## Chatbot Testing

- Start testing the La Liga Chatbot. Join this [page](https://www.facebook.com/La-Liga-Chatbot-Page-468645753642557/) and start chatting! Hope you enjoy it!


## Details

1. Crawl the teams data by following the links of each team's wikipedia page in the [La Liga wikipedia page](https://en.wikipedia.org/wiki/La_Liga?oldformat=true)

2. Write the inents examples under all these three given intents `great`,`laliga_questions`, `city_questions` and `thankyou`
	- `great`: User is greating the bot
	- `laliga_questions`: User's questions about the history of La Liga Clubs
	- `city_questions`: User's questions about the city
	- `thankyou`: User is thanking the bot
	__Note__: That we could add as much intents as we want, this is something you decide based on the domain of your chatbot 

3. Define the configuration of the [Rasa NLU pipeline](https://rasa.com/docs/nlu/choosing_pipeline/) in the `laliga_intents_config.yml` , I defined my NLU pipeline that builds the intent classifier as following:
	- Message Tokenization
	- POS tagging
	- Glove vectors extracted for each token
	- Concatentate those vecotrs to form a feature vector for each sentence
	- Build a multiclass SVM model for intent classification
	- CRF trained on message tokens ans POS tags for entity extraction

4. Build and user intent classifier to classifiy the user message as one of three given intents `great`,`laliga_questions`, `city_questions` and `thankyou`
	- using the following command
		`python -m rasa_nlu.train -c laliga_intents_config.yml --data laliga_intents.md -o models --fixed_model_name nlu --project current --verbose`
	- this command create a directory `./models/current/nlu` where the model and its metadata resides
	- then using `rasa_nlu.model.Interpreter` module I generate the intent of the message and its confidence ratio

5. Using [spacy multi-language model](https://spacy.io/models/xx) I attempt to extract intities in the user message like `LOC`, `ORG` and `PER` which will help along side the `intent_comfidence` and `intent_type` to decide on the most suitable reply to return to the user given the intent is `laliga_questions` offcourse
	- Download the multi-language model using the following command:
		`python -m spacy download xx_ent_wiki_sm`



## Project WD Components

1. `crawl.py` : the crawler that I used to crawl the teams data including (team name, team wikipedia page link, a summary about team and the history of the team)
	- To build this crawler I used the following tools [wikipedia](https://pypi.org/project/wikipedia/) which is a MediaWiki API python wrapper and Beautifulsoup

2. The intents examples are in `laliga_intents.md` where each intent example is written as the following example:
	```
	## intent:thankyou
	- Thanks so much!
	```
3. `core.py` contains the core of the chatbot as in `get_bot_response(message)` which returns the chatbot reply after recieving the user message		

4. `app.py` contains the code that connects the Facebook messenger API with [`ngrok`](https://ngrok.com/) then `Flask server` to the La Liga chatbot which sends its responses back to the user through th [`Pymessenger`](https://github.com/davidchua/pymessenger)python wrapper




## Some Notes on the behavior of the La Liga Chatbot

-  The chatbot is not resilient/ immune to spelling mistakes
-  I am planning to implement a different way to decide on the most suitable reply to return which uses the wordvectors of the club names and compare it to the extracted entities from the user message/ question. Unfortunaltely due to memory limitstion I wasnot able to go all the way through this approach
- I am also planning to build an end-to-end deep learning system that shoud be abe to convey more open conversation about the La Liga clubs including 
	- ` What team is [player]playing for ?`
	- ` List of players of [team]`
	- `What is the stadium of [team] ?`
	- ` What team is [stadium] of ?`
	- ` Who is the coach of [team] ?`
	- ` What team is coached by [coach] ?`
	- ` Get fixtures of [team]`
