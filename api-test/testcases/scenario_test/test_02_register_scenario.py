import allure
import pytest

from common.logger import logger
from common.redis_util import RedisClient
from operation.system import close_sys_register
from operation.user import acquire_login_verify_code, expire_login_verify_code, register

CAPTCHA_CODE_KEY = "captcha_codes:"
REDIS_CLIENT = RedisClient()


@allure.step("步骤1 ==>> 获取验证码")
def acquire_verify_code():
    """
    获取验证码
    :return:
    """
    verify_code, uuid = acquire_login_verify_code()
    logger.info("步骤1 ==>> 获取验证码：{}".format(verify_code))
    return verify_code, uuid


@allure.step("步骤2 ==>> 刷新验证码")
def refresh_verify_code():
    """
    刷新验证码
    :return:
    """
    verify_code, uuid = acquire_login_verify_code()
    logger.info("步骤2 ==>> 刷新验证码：{}".format(verify_code))
    return uuid


@allure.step("步骤2 ==>> 验证码失效")
def expire_verify_code(uuid: str):
    """
    让验证码失效
    :param uuid: 唯一请求
    :return:
    """
    expire_login_verify_code(uuid)
    logger.info("步骤2 ==>> 验证码失效")


@allure.step("步骤2 ==>> 关闭注册功能")
def close_register():
    """
    关闭系统注册功能
    :return:
    """
    close_sys_register()
    logger.info("步骤2 ==>> 关闭注册功能")


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：获取验证码-用户注册")
class TestUserLogin:

    @allure.story("用例--获取验证码/用户注册--预期成功")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("delete_register_user")
    def test_register_user_success(self, testcase_data):
        """
        用户注册-成功
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        result = register(username=username,
                          password=password,
                          confirm_password=password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 3. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        # 4. 验证注册后验证码是否失效
        assert REDIS_CLIENT.get(CAPTCHA_CODE_KEY + uuid) is None

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--获取验证码/用户注册--密码长度必须在5到20个字符之间")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-密码长度必须在5到20个字符之间")
    @pytest.mark.multiple
    def test_register_user_password_invalid(self, testcase_data):
        """
        用户注册-密码长度必须在5到20个字符之间
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        result = register(username=username,
                          password=password,
                          confirm_password=password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 3. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--获取验证码/用户注册--确认密码失败")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-确认密码失败")
    # 该
    @pytest.mark.skip
    @pytest.mark.usefixtures("delete_register_user")
    def test_register_user_confirm_password_not_same(self, testcase_data):
        """
        用户注册-确认密码失败
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        confirm_password = testcase_data["confirm_password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        result = register(username=username,
                          password=password,
                          confirm_password=confirm_password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 3. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--获取验证码/用户注册--没有开启注册功能")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-没有开启注册功能")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("restart_register_function")
    def test_register_user_sys_not_support_register(self, testcase_data):
        """
        用户注册-没有开启注册功能
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        # 3. 关闭系统注册功能
        close_register()

        result = register(username=username,
                          password=password,
                          confirm_password=password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 4. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--获取验证码/用户注册--验证码错误")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-验证码错误")
    @pytest.mark.multiple
    def test_register_user_verify_code_error(self, testcase_data):
        """
        用户注册-没有开启注册功能
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        # 3. 刷新验证码 模拟错误
        uuid = refresh_verify_code()

        result = register(username=username,
                          password=password,
                          confirm_password=password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 4. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--获取验证码/用户注册--验证码失效")
    @allure.description("该用例是针对 获取验证码/用户注册 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户获取验证码注册查看-验证码失效")
    @pytest.mark.multiple
    def test_register_user_verify_code_expired(self, testcase_data):
        """
        用户注册-没有开启注册功能
        :param testcase_data 测试数据
        :return:
        """

        # 1. 变量初始化
        username = testcase_data["username"]
        password = testcase_data["password"]
        except_code = testcase_data["except_code"]
        except_msg = testcase_data["except_msg"]

        logger.info("*************** START-TEST ***************")

        # 2. 获取验证码
        verify_code, uuid = acquire_verify_code()

        # 3. 验证码失效
        expire_verify_code(uuid=uuid)

        result = register(username=username,
                          password=password,
                          confirm_password=password,
                          verify_code=verify_code,
                          uuid=uuid)
        # 4. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_register_scenario.py"])
