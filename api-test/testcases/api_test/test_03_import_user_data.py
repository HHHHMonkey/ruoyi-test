import os

import allure
import pytest

from common.logger import logger
from operation.user import upload
from testcases.conftest import api_data

# 导入文件的路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
IMPORT_DATA_PATH = os.path.join(BASE_PATH, "excel")


@allure.step("步骤1 ==>> 批量导入用户数据")
def step_1():
    logger.info("步骤1 ==>> 批量导入用户数据")


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("批量导入用户数据")
class TestImportUserData:
    """获取用户信息模块"""

    @allure.story("用例--批量导入用户数据")
    @allure.description("该用例是针对批量导入用户数据接口的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @pytest.mark.single
    @pytest.mark.parametrize("filename, except_code", api_data["test_import_user_data"])
    @pytest.mark.usefixtures("delete_import_user")
    def test_import_user_data(self, get_login_token, filename, except_code):
        """
        批量导入用户数据
        :param get_login_token: 登陆token
        :param filename: 文件路径
        :param except_code: 期望返回code
        :return:
        """
        logger.info("*************** START-TEST ***************")

        token = get_login_token
        step_1()

        result = upload(filename=os.path.join(IMPORT_DATA_PATH, filename), token=token)

        assert result.response.json().get("code") == except_code
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))

        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_import_user_data.py"])
