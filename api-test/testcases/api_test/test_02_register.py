import allure
import pytest

from common.logger import logger
from operation.user import register
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 注册用户")
def step_1(username, password, confirmPassword):
    logger.info("步骤1 ==>> 注册用户 ==>> {}, {}, {}".format(username, password, confirmPassword))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("用户注册模块")
class TestUserRegister:
    """用户注册"""

    @allure.story("用例--注册用户信息")
    @allure.description("该用例是针对获取用户注册接口的测试")
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @allure.title(
        "测试数据：【 {username}, {password}, {confirmPassword}, {except_code}, {except_msg}】")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, confirmPassword, except_code, except_msg",
                             api_data["test_register_user"])
    @pytest.mark.usefixtures("delete_register_user")
    def test_register_user(self, username, password, confirmPassword, except_code, except_msg):
        logger.info("*************** 开始执行用例 ***************")
        result = register(username, password, confirmPassword)
        step_1(username, password, confirmPassword)
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg
        logger.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_code, result.response.json().get("code")))
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_register.py"])
