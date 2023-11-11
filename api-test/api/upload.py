import os

from common.read_data import data
from core.rest_client import RestClient

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]


class Upload(RestClient):

    def __init__(self, api_root_url, **kwargs):
        super(Upload, self).__init__(api_root_url, **kwargs)

    def import_user_data(self, **kwargs):
        return self.post("/system/user/importData", **kwargs)


upload_api = Upload(api_root_url)
