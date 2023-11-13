import allure
import pytest

from common.logger import logger
from operation.user import register, acquire_login_verify_code
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 注册用户")
def step_1(username, password, confirm_password):
    logger.info("步骤1 ==>> 注册用户 ==>> {}, {}, {}".format(username, password, confirm_password))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("用户注册模块")
class TestUserRegister:
    """
    用户注册
    """

    @allure.story("用例--注册用户信息")
    @allure.description("该用例是针对获取用户注册接口的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试数据：[{username}, {password}, {confirm_password}, {except_code}, {except_msg}]")
    @pytest.mark.single
    @pytest.mark.parametrize("username, password, confirm_password, except_code, except_msg",
                             api_data["test_register_user"])
    @pytest.mark.usefixtures("delete_register_user")
    def test_register_user(self, username, password, confirm_password, except_code, except_msg):
        """
        用户注册
        :param username: 用户名称
        :param password: 密码
        :param confirm_password: 确认密码
        :param except_code: 期望返回code
        :param except_msg: 期望返回msg
        :return:
        """
        logger.info("*************** START-TEST ***************")

        step_1(username, password, confirm_password)
        verify_code, uuid = acquire_login_verify_code()

        result = register(username=username,
                          password=password,
                          confirm_password=confirm_password,
                          verify_code=verify_code,
                          uuid=uuid)

        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))

        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_register.py"])
