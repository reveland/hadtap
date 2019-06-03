import logging
from hadtap.provider.sheet_provider import SheetProvider
from hadtap.handler.handler import Handler
from gspread.exceptions import CellNotFound
from hadtap.handler.newcomer_handler import NewcomerHandler

logger = logging.getLogger(__name__)


class MessageHandler(Handler):

    def __init__(self):
        self.sheet_provider = SheetProvider()
        self.newcomer_handler = NewcomerHandler(self.sheet_provider)

    def handle(self, user_id, message):
        if user_id not in self.sheet_provider.get_user_ids():
            logger.debug('user not found: %s', user_id)
            return self.newcomer_handler.handle(user_id, message)
        else:
            try:
                value = self.sheet_provider.get_value_for_item(message)
                if value is None:
                    return 'Nincs ilyen arucikk.'
                user_name = self.sheet_provider.get_name(user_id)
                logger.debug('record value for user: %s, %s', value, user_name)
                self.sheet_provider.record_fogyasztas(user_name, value)
                logger.info('fogyasztas recorded for %s: %s', user_id, value)
                return 'done.'
            except CellNotFound:
                return 'Valoszinuleg rossz nevet adtal meg, szolj Revinek.'
