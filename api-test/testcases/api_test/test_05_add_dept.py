import allure
import pytest

from common.logger import logger
from operation.system import add_dept
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
    @allure.title(
        "测试数据：【 {parentId}，{deptName}，{orderNum}，{leader}, {phone}, {email}, {status}, {expect_code}, {expect_msg}】")
    @pytest.mark.single
    @pytest.mark.parametrize("parentId, deptName, orderNum, leader, phone, email, status, expect_code, expect_msg",
                             api_data["test_add_dept"])
    @pytest.mark.usefixtures("delete_add_dept")
    def test_add_dept(self, get_login_token,
                      parentId,
                      deptName,
                      orderNum,
                      leader,
                      phone,
                      email,
                      status,
                      expect_code,
                      expect_msg):
        """
        :param get_login_token:
        :param parentId:
        :param deptName:
        :param orderNum:
        :param leader:
        :param phone:
        :param email:
        :param status:
        :param expect_code:
        :param expect_msg:
        :return:
        """
        logger.info("*************** START-TEST ***************")

        token = get_login_token
        result = add_dept(parentId=parentId,
                          deptName=deptName,
                          orderNum=orderNum,
                          leader=leader,
                          phone=phone,
                          email=email,
                          status=status,
                          token=token)
        logger.info("code ==>> expect: [{}]， actual: [{}]".format(expect_code, result.response.json().get("code")))
        assert result.response.json().get("code") == expect_code
        assert result.response.json().get("msg") == expect_msg

        logger.info("*************** END-TEST ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_05_add_dept.py"])
