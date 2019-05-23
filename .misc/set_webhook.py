from pprint import pprint
import requests

bot_token = '654997238:AAEoY9SqPsKXkST1DS3tfTUwl-O3xxxLecA'
test_url = "https://hadtap.herokuapp.com/{}".format(bot_token)


def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(bot_token, method)


r = requests.get(get_url("setWebhook"), data={"url": test_url})
r = requests.get(get_url("getWebhookInfo"))
pprint(r.status_code)
pprint(r.json())
