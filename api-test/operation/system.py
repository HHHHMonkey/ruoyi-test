from api.system import system_api
from common.logger import logger
from common.redis_util import RedisClient
from core.result_base import ResultBase

# False/True: 关闭/开启
REGISTER_STATUS_KEY = "sys_config:sys.account.registerUser"

REDIS_CLIENT = RedisClient()


def change_job_status(job_id: int, status: int, token: str) -> ResultBase:
    """
    根据id,status去修改定时任务的状态
    :param job_id: 任务ID
    :param status: 状态0:开启/1:关闭
    :param token: 登陆token
    :return:
    """

    result = ResultBase()

    header = {
        "Content-Type": "application/json",
        "Authorization": token,
    }

    payload = {
        "jobId": job_id,
        "status": status
    }

    res = system_api.change_job_status(json=payload, headers=header)
    result.success = True

    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("用户注册 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result


def add_dept(parentId: int,
             deptName: str,
             orderNum: int,
             leader: str,
             phone: str,
             email: str,
             status: str,
             token: str) -> ResultBase:
    """
    添加部门
    :param token: 登陆token
    :param parentId: 父部门Id
    :param deptName: 部门名称
    :param orderNum: 排序数字
    :param leader: 领导人名称
    :param phone: 电话
    :param email: 邮箱
    :param status: 部门
    :return:
    """

    result = ResultBase()

    header = {
        "Content-Type": "application/json",
        "Authorization": token,
    }

    payload = {
        "parentId": parentId,
        "deptName": deptName,
        "email": email,
        "leader": leader,
        "orderNum": orderNum,
        "phone": phone,
        "status": status
    }

    res = system_api.add_dept(json=payload, headers=header)
    result.success = True

    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("添加部门 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result


def close_sys_register():
    """
    关闭系统注册的功能
    :return:
    """
    REDIS_CLIENT.set(REGISTER_STATUS_KEY, "false")


def open_sys_register():
    """
    打开系统注册的功能
    :return:
    """
    REDIS_CLIENT.set(REGISTER_STATUS_KEY, "true")
