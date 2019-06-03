import logging
from hadtap.handler.handler import Handler

logger = logging.getLogger(__name__)


class NewcomerHandler(Handler):

    def __init__(self, provider):
        self.provider = provider

    def handle(self, user_id, message):
        names = self.provider.get_names()
        if message not in names:
            return 'Szia, mi a neved?'
        else:
            self.provider.add_newcomer(message, user_id)
            return 'Szuper, koszi'
