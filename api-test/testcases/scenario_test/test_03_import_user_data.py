import os

import allure
import pytest

from common.logger import logger
from operation.user import upload

# 导入文件的路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
IMPORT_DATA_PATH = os.path.join(BASE_PATH, "excel")


@allure.step("步骤1 ==>> 获取需要导入的数据文件")
def acquire_import_data_file(file):
    logger.info("步骤1 ==>> 获取需要导入的数据文件:{}".format(file))


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：用户登陆-用户数据导入")
class TestUserLogin:

    @allure.story("用例--用户登陆-用户数据导入--预期成功")
    @allure.description("该用例是针对 用户登陆-用户数据导入 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户登陆-用户数据导入-预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("delete_import_user")
    def test_import_user_data_success(self, get_login_token, testcase_data):
        """
        批量导入用户数据-成功
        :param get_login_token: 登陆token
        :param testcase_data 测试数据
        :return:
        """
        logger.info("*************** START-TEST ***************")

        # 1. 变量初始化
        file = testcase_data["file"]
        except_code = testcase_data["except_code"]

        # 2. 获取登陆token
        token = get_login_token

        # 3. 获取需要导入的数据文件
        acquire_import_data_file(file)

        # 4. 上传
        result = upload(filename=os.path.join(IMPORT_DATA_PATH, file), token=token)

        # 5. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--用户登陆-用户数据导入--重复导入")
    @allure.description("该用例是针对 用户登陆-用户数据导入 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户登陆-用户数据导入-重复导入")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("delete_import_user")
    def test_import_user_data_replicate_import(self, get_login_token, testcase_data):
        """
        批量导入用户数据-重复导入
        :param get_login_token: 登陆token
        :param testcase_data 测试数据
        :return:
        """
        logger.info("*************** START-TEST ***************")

        # 1. 变量初始化
        file = testcase_data["file"]
        except_code = testcase_data["except_code"]

        # 2. 获取登陆token
        token = get_login_token

        # 3. 获取需要导入的数据文件
        acquire_import_data_file(file)

        # 4. 上传
        result = upload(filename=os.path.join(IMPORT_DATA_PATH, file), token=token)

        # 5. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code

        logger.info("*************** END-TEST ***************")

    @allure.story("用例--用户登陆-用户数据导入--空文件")
    @allure.description("该用例是针对 用户登陆-用户数据导入 场景的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("用户登陆-用户数据导入-空文件")
    @pytest.mark.multiple
    def test_import_user_data_empty(self, get_login_token, testcase_data):
        """
        批量导入用户数据-空文件
        :param get_login_token: 登陆token
        :param testcase_data 测试数据
        :return:
        """
        logger.info("*************** START-TEST ***************")

        # 1. 变量初始化
        file = testcase_data["file"]
        except_code = testcase_data["except_code"]

        # 2. 获取登陆token
        token = get_login_token

        # 3. 获取需要导入的数据文件
        acquire_import_data_file(file)

        # 4. 上传
        result = upload(filename=os.path.join(IMPORT_DATA_PATH, file), token=token)

        # 5. 断言
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code

        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_import_user_data.py"])
