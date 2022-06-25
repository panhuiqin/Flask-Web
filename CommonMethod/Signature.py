# -*- coding: utf-8 -*-
import time
from hashlib import sha1
import random
import copy
import json

class SignatureEncryption:

    @classmethod
    def get_sign(cls, data) :
        """  获取签名方法
        :return:输入签名sign
        """
        timestamp = str(int(time.time()))
        nonce1 = str(random.randint(0, 99))
        # nonce1 = random.randint(0, 99)
        # data = json.loads(data)
        # data = dict(data)
        data_copy = data
        if isinstance(data_copy, str):
            data_copy = json.loads(data_copy)
        parameter = copy.deepcopy(data_copy)
        parameter.setdefault("nonce", nonce1)
        parameter.setdefault("timestamp", timestamp)

        # for l in parameter.keys():
        #     if not isinstance(parameter[l], str):
        #         # parameter[l] = json.dumps(parameter[l])
        #         print(parameter[l])
        #         str_1 = json.dumps(parameter[l])
        #         str_1.replace('\\','\\\\')
        #         str_1.replace('"','\"')
        #         parameter[l] = str_1


        # sort_b1 = sorted(parameter, key=lambda s: s[0])
        sort_b = sorted(parameter)  # 对对象进行排序
        body = ''
        for i in sort_b :
            parameters_body = "{0}={1}&".format(i, parameter[i])
            body = body + parameters_body
        # print(body)
        # print(body[:-1])
        s1 = sha1()  # 创建sha1加密对象
        # print(body[:-1])
        s1.update(body[:-1].encode("utf-8"))  # 转码（字节流）
        password2 = s1.hexdigest().upper()  # 将字节码转成16进制
        # print(password2.upper())
        ulr_sign1 = '?{0}={1}&{2}={3}&{4}={5}'.format('nonce', nonce1, 'timestamp', timestamp, 'sign', password2)
        ulr_sign = {"nonce" : nonce1, "timestamp" : timestamp, "sign" : password2, "Splicing": ulr_sign1}
        # print(ulr_sign)
        return ulr_sign