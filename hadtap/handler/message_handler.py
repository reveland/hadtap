import logging
from kalandor.provider.sheet_provider import SheetProvider
from kalandor.handler.handler import Handler
from kalandor.handler.newcomer_handler import NewcomerHandler

logger = logging.getLogger(__name__)


class MessageHandler(Handler):

    def __init__(self):
        self.sheet_provider = SheetProvider()
        self.newcomer_handler = NewcomerHandler(self.sheet_provider)

    def handle(self, user_id, message):
        if user_id not in self.sheet_provider.get_user_ids():
            return self.newcomer_handler.handle(user_id, message)
        else:
            value = self.sheet_provider.get_value_for_item(message)
            if value is None:
                return 'sry bro: %s nincs a listán', message
            user_name = self.sheet_provider.get_name(user_id)
            self.record_fogyasztas(user_name, value)
            logger.info('fogyasztas recorded for %s: %s', user_id, value)
