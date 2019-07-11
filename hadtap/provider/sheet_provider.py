import os
import ast
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from hadtap.provider.provider import Provider

logger = logging.getLogger(__name__)


class SheetProvider(Provider):

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        creds_dict = ast.literal_eval(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, scope)
        client = gspread.authorize(creds)

        sheet_key = os.environ['SHEET_KEY']
        user_sheet_key = os.environ['USER_SHEET_KEY']
        self.document = client.open_by_key(sheet_key)
        self.user_document = client.open_by_key(user_sheet_key)
        self.fogyasztas_sheet = self.document.sheet1
        self.user_sheet = self.user_document.sheet1
        self.item_sheet = self.user_document.worksheet('items')

    def get_names(self):
        return self.fogyasztas_sheet.row_values(1)

    def get_user_ids(self):
        ids = self.user_sheet.col_values(2)
        logger.debug('user_ids: %s', ids)
        return ids

    def record_fogyasztas(self, user_name, value):
        logger.debug('record for %s: %s', user_name, value)
        col_ = self.fogyasztas_sheet.find(user_name).col
        fogyasztasok = self.fogyasztas_sheet.col_values(col_)
        row_ = len(fogyasztasok)
        logger.debug('update cell: %s, %s to %s', row_, col_, value)
        self.fogyasztas_sheet.update_cell(row_ + 1, col_, value)
        return int(fogyasztasok[3]) + int(value)

    def get_value_for_item(self, item):
        try:
            item_cell = self.item_sheet.find(item)
            return self.item_sheet.cell(item_cell.row, 2).value
        except:
            return None

    def get_items(self):
        names = self.item_sheet.col_values(1)
        values = self.item_sheet.col_values(2)
        return list(map(lambda x: '-'.join(x), zip(names, values)))

    def get_name(self, user_id):
        user_cell = self.user_sheet.find(str(user_id))
        user_name = self.user_sheet.cell(user_cell.row, 1).value
        logger.debug('got name for id: %s, %s', user_name, user_id)
        return user_name

    def add_newcomer(self, user_name, user_id):
        logger.debug('add newcomer: %s, %s', user_id, user_name)
        self.user_sheet.append_row([user_name, user_id])

    def record_action(self, user_id, action):
        row_index = self.user_sheet.find(user_id).row
        actions = self.user_sheet.cell(row_index, 3).value
        updated_actions = actions + '#' + action
        self.user_sheet.update_cell(row_index, 3, updated_actions)
        logger.info('action recorded for %s: %s', user_id, action)
