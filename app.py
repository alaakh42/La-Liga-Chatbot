#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
from core import get_bot_response, get_bot_response_nonTexts

app = Flask(__name__)

ACCESS_TOKEN = 'EAAewPyxbNooBAGScp9vPUJiTZClCn6SFsA2PO6lCyTwouZCGn754vDrvh8ZCxqfp0agxUsG4nwdbfok1pmcZAG6AtNIs8gk87Ew04NhzfTmcD04qnFGg2EttihqVYVkOPwopTjOggyop4CGqQdIL5NZCI6isCJF8wtsZAal0kCrAZDZD'
VERIFY_TOKEN = "AMmVd7vSvYBR75oe1/DfS/wB+rM+/aPAj4WxNl05PW8="
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    if request.method == 'POST':
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    print(message['message'].get('text'))
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                # if message['message'].get('attachments'):
                #     # for att in message['message'].get('attachments'):
                #         # print(att)
                #     print(message['message'].get('attachments'))
                #     msg, image_url = get_nontxt_message(message['message'].get('attachment'))
                #     print(msg, image_url)
                    # send_message(recipient_id, msg)
                    # send_nontxt_message(recipient_id, image_url)
            else:
                pass

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(message):
    # return bot response to the user
    # given text data
    return get_bot_response(message) 

def get_nontxt_message(message):
    # return bot response to the user 
    # given non-text data
    return get_bot_response_nonTexts(message)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def send_nontxt_message(recipient_id, image_url):
    #sends user the non-text message provided via input image_url parameter
    bot.send_image_url(recipient_id, image_url)
    return "success"


if __name__ == "__main__":
    app.run(port=8888, debug=True)
