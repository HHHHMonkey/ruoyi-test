import http

from api.user import user_api
from common.logger import logger
from common.redis_util import RedisClient
from core.result_base import ResultBase

CAPTCHA_CODE_KEY = "captcha_codes:"

REDIS_CLIENT = RedisClient()


def upload(filename, token) -> ResultBase:
    """
    通过excel文件批量添加用户(前端控制了一次只能上传一个文件)
    :param token: 登陆token
    :param filename: 上传的文件路径
    :return:
    """
    result = ResultBase()

    # 注意不需要再使用"Content-Type": "multipart/form-data",
    # 谷歌浏览器会自动帮你添加该属性
    header = {
        "Authorization": token,
    }

    files = {
        "file": open(filename, 'rb')
    }

    res = user_api.import_user_data(files=files, headers=header)

    logger.info("upload response json is {}".format(res.json()))
    result.success = False

    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("批量导入用户数据 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result


def register(username, password, confirm_password, verify_code, uuid) -> ResultBase:
    """
    用户注册
    :param uuid: 唯一请求id
    :param verify_code: 验证码
    :param confirm_password: 确认的密码
    :param username: 用户名
    :param password: 密码
    :return:
    """
    result = ResultBase()

    payload = {
        "username": username,
        "password": password,
        "confirmPassword": confirm_password,
        "code": verify_code,
        "uuid": uuid
    }

    header = {
        "Content-Type": "application/json"
    }

    res = user_api.register(json=payload, headers=header)
    result.success = False

    if res.json()["code"] == 0:
        result.success = True
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("用户注册 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result


def login(username: str, password: str, verify_code: str, uuid: str) -> ResultBase:
    """
    用户登陆
    :param username: 用户名
    :param password: 密码
    :param verify_code: 验证码
    :param uuid: 唯一id
    :return: ResultBase
    """
    result = ResultBase()

    payload = {
        "username": username,
        "password": password,
        "code": verify_code,
        "uuid": uuid
    }

    header = {
        "Content-Type": "application/json"
    }

    res = user_api.login(json=payload, headers=header)
    result.success = False

    if res.json()["code"] == 0:
        result.success = True
        result.token = res.json()["token"]
    else:
        result.error = "接口返回码是 [{}], 返回信息：{} ".format(res.json()["code"], res.json()["msg"])

    result.msg = res.json()["msg"]
    result.response = res
    logger.info("用户登陆 ==>> 返回结果 ==>> {}".format(result.response.text))

    return result


def acquire_login_verify_code() -> (str, str):
    """
    获取验证码
    :return: verify code
    """

    # 准备请求头
    header = {
        "Content-Type": "application/json"
    }

    # 获取验证码
    response = user_api.captchaImage(headers=header)

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


def expire_login_verify_code(uuid: str):
    """
    :param uuid 唯一请求id
    让验证码失效
    :return:
    """
    REDIS_CLIENT.delete(key=CAPTCHA_CODE_KEY + uuid)
