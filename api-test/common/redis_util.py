import os

import redis

from common.read_data import data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
data = data.load_ini(data_file_path)["redis"]

DB_CONF = {
    "host": data["REDIS_HOST"],
    "port": int(data["REDIS_PORT"]),
}


class RedisClient:
    """
    提供读取和设置redis-kv的功能
    """

    def __init__(self, host=DB_CONF["host"], port=DB_CONF["port"]):
        self.__redis = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def set(self, key, value):
        return self.__redis.set(key, value)

    def get(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return None

    def delete(self, key):
        if self.__redis.exists(key):
            return self.__redis.delete(key)
        else:
            return None
