import allure
import pytest

from common.logger import logger
from operation.system import change_job_status
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 开启后台定时任务")
def step_1(username):
    logger.info("步骤1 ==>> 开启后台定时任务：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("定时任务模块")
class TestCronJob:

    @allure.story("用例--开启定时任务")
    @allure.description("该用例是针对开启定时任务接口的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title("测试数据：[{job_id}，{status}，{except_code}，{except_msg}]")
    @pytest.mark.single
    @pytest.mark.parametrize("job_id, status, except_code, except_msg", api_data["test_change_job_status"])
    def test_change_job_status(self, get_login_token, job_id, status, except_code, except_msg):
        """
        开启后台定时任务
        :param get_login_token: 登陆token
        :param job_id: 定时任务id
        :param status: 定时任务状态0:开启/1:关闭
        :param except_code: 期望返回code
        :param except_msg: 期望返回msg
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
