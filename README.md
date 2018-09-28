# La Liga Clubs History Chatbot

This repo is an attemt to solve the Clubs history challenge!

This chatbot can have a comprehensive conversation with the user while giving him/ her some information about the history of La Liga Clubs

### Install Requirements

To install the project dependencies, run the following command
	`sudo -H pip install -r requirements.txt`

## Details

1. Crawl the teams data by following the links of each team's wikipedia page in the [La Liga wikipedia page](https://en.wikipedia.org/wiki/La_Liga?oldformat=true)

2. Write the inents examples under all these three given intents `great`,`laliga_questions`, `city_questions` and `thankyou`
	- `great`: User is greating the bot
	- `laliga_questions`: User's questions about the history of La Liga Clubs
	- `city_questions`: User's questions about the city
	- `thankyou`: User is thanking the bot
	_Note_: That we could add as much intents as we want, this is something you decide based on the domain of your chatbot 

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

5. Using [spacy multi-language model](https://spacy.io/models/xx) I attempt to extract intities in the user message like `LOC` and `ORG` which will help me decide the most suitable reply to return to the user given the intent is `laliga_questions` offcourse
	- Download the multi-language model using the following command:
		`python -m spacy download xx_ent_wiki_sm`



## Project WD Components

1. `crawl.py` : the crawler that I used to crawl the teams data including (team name, team wikipedia page link, a summary about team and the history of the team)
	- To build this crawler I used the following tools [wikipedia](https://pypi.org/project/wikipedia/) which is a MediaWiki API python wrapper and Beautifulsoup

2. The intents examples are in `laliga_intents.md` where each intent example is written as the following example:
	## intent:thankyou
	- Thanks so much!

3. `core.py` contains the core of the chatbot as in `get_bot_response(message)` which returns the chatbot reply after recieving the user message		

4. `server.py` contains the code that connects the Facebook messenger API with `ngrok` then `Flask server` to the La Liga chatbot which sends its responses back to the user using the python package `requests` that help send messages as http requests



