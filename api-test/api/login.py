import os

from common.read_data import data
from core.rest_client import RestClient

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]


class Login(RestClient):

    def __init__(self, api_root_url, **kwargs):
        super(Login, self).__init__(api_root_url, **kwargs)

    def login(self, **kwargs):
        return self.post("/login", **kwargs)

    def captchaImage(self, **kwargs):
        return self.get("/captchaImage", **kwargs)


login_api = Login(api_root_url)
