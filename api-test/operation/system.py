from api.monitor import monitor_api
from api.system import system_api
from common.logger import logger
from core.result_base import ResultBase


def change_job_status(job_id: int, status: int, token: str) -> ResultBase:
    """
    根据id,status去修改定时任务的状态
    :param job_id:
    :param status:
    :param token:
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

    res = monitor_api.change_job_status(json=payload, headers=header)
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
    :param token:
    :param parentId:
    :param deptName:
    :param orderNum:
    :param leader:
    :param phone:
    :param email:
    :param status:
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
