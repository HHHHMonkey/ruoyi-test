import allure
import pytest

from common.logger import logger
from operation.user import login
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 登录用户")
def step_1(username):
    logger.info("步骤1 ==>> 登录用户：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("用户登录模块")
class TestUserLogin:

    @allure.story("用例--登录用户-成功")
    @allure.description("该用例是针对获取用户登录成功的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试数据：[{username}，{password}，{except_code}，{except_msg}] ")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, except_code, except_msg", api_data["test_login_user"])
    def test_login_user_success(self, username, password, except_code, except_msg):
        """
        用户登陆
        :param username: 用户名称
        :param password: 密码
        :param except_code: 期望返回code
        :param except_msg: 期望返回msg
        :return:
        """
        logger.info("*************** START-TEST ***************")
        result = login(username, password)
        step_1(username)
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg
        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_login.py"])
