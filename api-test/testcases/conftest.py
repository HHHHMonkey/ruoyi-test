import os

import allure
import pytest

from api.user import user_api
from common.logger import logger
from common.mysql_operate import db
from common.read_data import data
from operation.system import open_sys_register
from operation.user import acquire_login_verify_code

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


base_data = get_data("base_data.yml")
api_data = get_data("api_test_data.yml")
scenario_data = get_data("scenario_test_data.yml")


@allure.step("前置步骤 ==>> 清理数据")
def step_first():
    logger.info("******************************")
    logger.info("前置步骤开始 ==>> 清理数据")


@allure.step("后置步骤 ==>> 清理数据")
def step_last():
    logger.info("后置步骤开始 ==>> 清理数据")


@allure.step("前置步骤 ==>> 管理员用户登录")
def step_login(username, password):
    logger.info("前置步骤 ==>> 管理员 {} 登录，返回信息 为：{}".format(username, password))


@pytest.fixture(scope="session")
def get_login_token():
    """
    获取登陆token
    :return:
    """
    username = base_data["init_admin_user"]["username"]
    password = base_data["init_admin_user"]["password"]
    header = {
        "Content-Type": "application/json"
    }
    verify_code, uuid = acquire_login_verify_code()
    payload = {
        "username": username,
        "password": password,
        "code": verify_code,
        "uuid": uuid
    }
    response = user_api.login(json=payload, headers=header)
    step_login(username, password)
    yield response.json()["token"]


@pytest.fixture(scope="function")
def delete_import_user():
    """
    导入用户数据前，先删除数据，用例执行之后，再次删除以清理数据
    """
    del_sql = base_data["init_sql"]["delete_import_user"]
    db.execute_db(del_sql)
    step_first()
    logger.info("注册用户操作：清理用户--准备导入新用户")
    logger.info("执行前置SQL：{}".format(del_sql))
    yield
    db.execute_db(del_sql)
    step_last()
    logger.info("注册用户操作：删除导入的用户")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def delete_register_user():
    """
    注册用户前，先删除数据，用例执行之后，再次删除以清理数据
    """
    del_sql = base_data["init_sql"]["delete_register_user"]
    db.execute_db(del_sql)
    step_first()
    logger.info("注册用户操作：清理用户--准备注册新用户")
    logger.info("执行前置SQL：{}".format(del_sql))
    yield
    db.execute_db(del_sql)
    step_last()
    logger.info("注册用户操作：删除注册的用户")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def delete_add_dept():
    """
    增加部门前，先删除数据，用例执行之后，再次删除以清理数据
    """
    del_sql = base_data["init_sql"]["delete_add_dept"]
    db.execute_db(del_sql)
    step_first()
    logger.info("注册用户操作：清理用户--准备添加新部门")
    logger.info("执行前置SQL：{}".format(del_sql))
    yield
    db.execute_db(del_sql)
    step_last()
    logger.info("注册用户操作：删除添加的部门")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def restart_register_function():
    """
    关闭注册功能之后,需要重新打开
    """
    yield
    open_sys_register()
    logger.info("注册用户操作：打开系统注册用户功能")
