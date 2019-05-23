from flask import Flask, request, Response
import json
import logging.config
import os

from hadtap.chatbot.telegram_chatbot import TelegramChatBot
from hadtap.handler.message_handler import MessageHandler

with open('log_config.json', 'r') as log_config_json:
    log_config_dict = json.load(log_config_json)
logging.config.dictConfig(log_config_dict)

logger = logging.getLogger(__name__)
app = Flask(__name__)
telegram_chatbot = TelegramChatBot()
message_handler = MessageHandler()


@app.route('/chat/')
def chat():
    message = request.args.get('message')
    logger.debug('local receive request: %s', message)
    answer = ''
    if message is not None:
        answer = message_handler.handle('547578996', message)
    logger.debug('local answer: %s', answer)
    form = """
            <form action="/chat">
                <input type="text" name="message"><br>
                <input type="submit" value="Submit">
            </form>
            %s
           """ % answer
    return form


@app.route("/{}".format(os.environ["TELEGRAM_API_TOKEN"]), methods=["POST"])
def telegram_hook():
    logger.debug('Telegram hook receive request: %s', request)
    message = telegram_chatbot.get_message(request)
    if message is not None:
        message['user_id'] = str(message['user_id'])
        logger.info('Telegram message receive from %s: %s',
                    message['user_id'], message['text'])
        # this is a chat_id not an user_id, telegram stuff
        answer = message_handler.handle(
            message['user_id'], message['text'])
        logger.info('Telegram answer send to %s', message['user_id'])
        logger.debug('%s', answer)
        telegram_chatbot.send_message(message['user_id'], answer)
    return Response(status=200)


if __name__ == '__main__':
    app.run()
