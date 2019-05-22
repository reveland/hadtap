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
        return self.user_sheet.col_values(1)

    def record_fogyasztas(self, user_name, value):
        col_ = self.fogyasztas_sheet.find(user_name).col
        self.fogyasztas_sheet.col_values(col_)
        row_ = len(self.fogyasztas_sheet.col_values(col_))
        self.fogyasztas_sheet.update_cell(row_, col_, value)

    def get_value_for_item(self, item):
        try:
            item = self.item_sheet.find('csoki')
            return self.item_sheet.cell(item.col, 2)
        except:
            return None

    def get_name(self, user_id):
        user = self.item_sheet.find(user_id)
        return self.item_sheet.cell(user.col, 2)
