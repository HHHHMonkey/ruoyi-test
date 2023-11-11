import allure
import pytest

from common.logger import logger
from operation.monitor import change_job_status
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 登录用户")
def step_1(username):
    logger.info("步骤1 ==>> 登录用户：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("定时任务模块")
class TestCronJob:

    @allure.story("用例--登录用户")
    @allure.description("该用例是针对获取用户登录接口的测试")
    @allure.issue("https://www.cnblogs.com/wintest", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://www.cnblogs.com/wintest", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试数据：【 {job_id}，{status}，{except_code}，{except_msg}】")
    @pytest.mark.single
    @pytest.mark.parametrize("job_id, status, except_code, except_msg", api_data["test_change_job_status"])
    def test_change_job_status(self, get_login_token, job_id, status, except_code, except_msg):
        """
        :param job_id:
        :param status:
        :param except_code:
        :param except_msg:
        :return:
        """
        logger.info("*************** START-TEST ***************")

        token = get_login_token
        result = change_job_status(job_id, status, token)

        logger.info("code ==>> expect: [{}]， actual: [{}]".format(except_code, result.response.json().get("code")))
        assert result.response.json().get("code") == except_code
        assert result.response.json().get("msg") == except_msg

        # TODO: 补充检查定时insert_sql的断言
        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_04_change_job_status.py"])
