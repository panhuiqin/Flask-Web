# -*- coding: utf-8 -*-
import requests
import json


class MessageNotification :

    @classmethod
    def msg_qw(cls, data) :
        """
        通知企业微信消息， 用例更新信息
        :parameter:data
        :return:
        """
        # 测试组机器人
        # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fbec70a5-0054-4274-b8ec-27440f6079e6"
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d173b823-7975-4fc6-ae6a-85e10e7b8275"
        content = "执行用例总数<font color=\"warning\">{0}</font>，请{4}项目测试的相关同事注意查看结果。\n>用例通过数:<font color=\"comment\">{1}</font>\n>用例失败数:<font color=\"comment\">{2}</font>\n>用例错误数:<font color=\"comment\">{3}</font>".format(
            str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]))
        payload = {
            "msgtype" : "markdown",
            "markdown" : {
                "content" : content,
                "mentioned_list" : ["@all"]
            }
        }
        headers = {
            'Content-Type' : 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    @classmethod
    def msg_qw_case(cls) :
        """
        通知企业微信消息， 用例更新信息
        :parameter:data
        :return:
        """
        # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=12b8ee03-210e-4de8-91b2-9798864f40a6"
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d173b823-7975-4fc6-ae6a-85e10e7b8275"
        payload = {
            "msgtype" : "text",
            "text" : {
                "content" : "用例状态更新失败，查看失败原因",
                "mentioned_list" : ["@all"]
            }
        }
        headers = {
            'Content-Type' : 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

