# -*-coding: utf-8 -*-
import connect_mysql.ConnectRedis as Cr
import json

class ExecuteRedis :

    def __init__(self):
        self.ConnectRedis = Cr.ConnectRedis()

    # name = "name"
    def Read_App_name(self):
        """
        获取rides，更新项目的项目名
        :return:
        """
        name = "name"
        try:
            req = self.ConnectRedis.Read_redis(name)
            return {"code" : "1", "msg" : "操作成功", "data" : str(req, encoding='utf-8')}
        except:
            return {"code":"99", "msg":"操作失败"}

    def Write_App_name(self, data) :
        """
        获取rides，更新项目的项目名
        :param data: 更新内容
        :return:
        """
        name = "name"
        try:
            self.ConnectRedis.Write_redis(name, data)
            return {"code" : "1", "msg" : "操作成功"}
        except:
            return {"code":"99", "msg":"操作失败"}

    def Read_App_token(self) :
        """
        获取rides，更新项目的token
        :return:
        """
        name = "token"
        try :
            req = self.ConnectRedis.Read_redis(name)
            return {"code" : "1", "msg" : "操作成功", "data" : str(req, encoding='utf-8')}
        except :
            return {"code" : "99", "msg" : "操作失败"}

    def Write_App_token(self, data) :
        """
        获取rides，更新项目的token
        :param data: 更新内容
        :return:
        """
        name = "token"
        try :
            self.ConnectRedis.Write_redis(name, data)
            # print({"code" : "1", "msg" : "操作成功"})
            return {"code" : "1", "msg" : "操作成功"}
        except :
            # print({"code" : "99", "msg" : "操作失败"})
            return {"code" : "99", "msg" : "操作失败"}

    def Write_App_data(self, data) :
        """
        获取rides，更新项目的token
        :param data: 更新内容
        :return:
        """
        name = "caseData"
        try :
            self.ConnectRedis.Write_redis(name, data)
            return {"code" : "1", "msg" : "操作成功"}
        except :
            return {"code" : "99", "msg" : "操作失败"}

    def Read_App_data(self) :
        """
        获取rides，更新项目的token
        :return:
        """
        name = "caseData"
        try :
            req = self.ConnectRedis.Read_redis(name)
            return {"code" : "1", "msg" : "操作成功", "data" : str(req, encoding='utf-8')}
        except :
            return {"code" : "99", "msg" : "操作失败"}
