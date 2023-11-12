import allure
import pytest

from common.logger import logger
from operation.system import add_dept
from testcases.conftest import api_data


@allure.step("步骤1 ==>> 系统添加部门")
def step_1(username):
    logger.info("步骤1 ==>> 系统添加部门：{}".format(username))


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对单个接口的测试")
@allure.feature("系统管理-添加部门")
class TestCronJob:

    @allure.story("用例--系统添加部门")
    @allure.description("该用例是针对系统添加部门接口的测试")
    @allure.issue("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应BUG的链接地址")
    @allure.testcase("https://github.com/WeiXiao-Hyy/ruoyi-test", name="点击，跳转到对应用例的链接地址")
    @allure.title(
        "测试数据：[{parentId}，{deptName}，{orderNum}，{leader}, {phone}, {email}, {status}, {expect_code}, {expect_msg}]")
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
        系统管理-添加部门
        :param get_login_token: 登陆token
        :param parentId: 父亲部门Id
        :param deptName: 部门名称
        :param orderNum: 排序数字
        :param leader: 领导人名称
        :param phone: 手机号码
        :param email: 邮件
        :param status: 部门状态 0:开启/1:关闭
        :param expect_code: 期望code
        :param expect_msg: 期望msg
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
