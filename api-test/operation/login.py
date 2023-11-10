import http

from api.login import login_api
from common.logger import logger
from common.redis_util import RedisClient
from core.result_base import ResultBase

CAPTCHA_CODE_KEY = "captcha_codes:"

REDIS_CLIENT = RedisClient()


def acquire_login_verify_code() -> (str, str):
    """
    :return: verify code
    """

    # prepare request parameter
    header = {
        "Content-Type": "application/json"
    }

    # captchaImage
    response = login_api.captchaImage(headers=header)

    verify_code = None
    uuid = None

    # construct redis-key(captcha_codes:uuid)
    if response.json()["code"] == http.HTTPStatus.OK:
        uuid = response.json()["uuid"]

        redis_key = CAPTCHA_CODE_KEY + uuid
        verify_code = REDIS_CLIENT.get(key=redis_key)

    logger.info("get verify_code={}, uuid={}".format(verify_code, uuid))

    # redis.get()存在b前置, 代表着bytes,需要转化为str
    return verify_code.replace("\\", "").replace("\"", ""), uuid


def login_user(username, password) -> ResultBase:
    """
    user login action
    :param username: 用户名
    :param password: 密码
    :return: ResultBase
    """
    result = ResultBase()

    # get verify code, uuid
    verify_code, uuid = acquire_login_verify_code()

    payload = {
        "username": username,
        "password": password,
        "code": verify_code,
        "uuid": uuid
    }

    header = {
        "Content-Type": "application/json"
    }
    res = login_api.login(json=payload, headers=header)
    result.success = False

    if res.json()["code"] == 0:
        result.success = True
        result.token = res.json()["login_info"]["token"]
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("登录用户 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result

# def update_user(id, admin_user, new_password, new_telephone, token, new_sex="", new_address=""):
#     """
#     根据用户ID，修改用户信息
#     :param id: 用户ID
#     :param admin_user: 当前操作的管理员用户
#     :param new_password: 新密码
#     :param new_telephone: 新手机号
#     :param token: 当前管理员用户的token
#     :param new_sex: 新性别
#     :param new_address: 新联系地址
#     :return: 自定义的关键字返回结果 result
#     """
#     result = ResultBase()
#     header = {
#         "Content-Type": "application/json"
#     }
#     json_data = {
#         "admin_user": admin_user,
#         "password": new_password,
#         "token": token,
#         "sex": new_sex,
#         "telephone": new_telephone,
#         "address": new_address
#     }
#     res = user.update(id, json=json_data, headers=header)
#     result.success = False
#     if res.json()["code"] == 0:
#         result.success = True
#     else:
#         result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
#     result.msg = res.json()["msg"]
#     result.response = res
#     logger.info("修改用户 ==>> 返回结果 ==>> {}".format(result.response.text))
#     return result
#
#
# def delete_user(username, admin_user, token):
#     """
#     根据用户名，删除用户信息
#     :param username: 用户名
#     :param admin_user: 当前操作的管理员用户
#     :param token: 当前管理员用户的token
#     :return: 自定义的关键字返回结果 result
#     """
#     result = ResultBase()
#     json_data = {
#         "admin_user": admin_user,
#         "token": token,
#     }
#     header = {
#         "Content-Type": "application/json"
#     }
#     res = user.delete(username, json=json_data, headers=header)
#     result.success = False
#     if res.json()["code"] == 0:
#         result.success = True
#     else:
#         result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["code"], res.json()["msg"])
#     result.msg = res.json()["msg"]
#     result.response = res
#     logger.info("删除用户 ==>> 返回结果 ==>> {}".format(result.response.text))
#     return result
