import os

import allure
import pytest

from common.logger import logger
from operation.user import upload
from testcases.conftest import api_data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


@allure.step("步骤1 ==>> 获取所有用户信息")
def step_1():
    logger.info("步骤1 ==>> 获取所有用户信息")


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("获取用户信息模块")
class TestImportUserData:
    """获取用户信息模块"""

    @allure.story("用例--获取全部用户信息")
    @allure.description("该用例是针对获取所有用户信息接口的测试")
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @pytest.mark.single
    @pytest.mark.parametrize("filename, except_code", api_data["test_import_user_data"])
    @pytest.mark.usefixtures("delete_import_user")
    def test_get_all_user_info(self, get_login_token, filename, except_code):
        logger.info("*************** START-TEST ***************")

        token = get_login_token
        step_1()

        # TODO:处理文件路径
        result = upload("/Users/hujiale/PycharmProjects/ruoyi-test/api-test/data/excel/import_user_data_success.xlsx",
                        token)

        assert result.response.json().get("code") == except_code
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        # print(result.__dict__)
        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_import_user_data.py"])
