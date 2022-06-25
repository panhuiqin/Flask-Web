import json
import os

import connect_mysql.ConnectDatabase as Cd
import CommonMethod.Signature as St
import method.CaseOperation as Co
import method.RedisOperation as Rd
import requests
import re
import random


def get_token_headers() :
    cursor, db = Cd.ConnectMysql().MysqlReadingWrite()
    sql = "select app_name, headers, auth_type, request_type, url, body from pro_info where app_name = 'DocGroup_scrm'"
    cursor.execute(sql)
    ab = cursor.fetchall()
    print(ab)
    return ab


def update_token_inside() :
    """
    内部调用接口，万能token
    :return:
    """
    url = "https://testauth.lian-ou.com/auth/login/token"
    payload = {
        "userName" : "testadmin",
        "password" : "lian0u!@#2022",
        "userType" : 10
    }
    headers = {
        'Content-Type' : 'application/json',
        'x-logw-env' : 'test',
        'x-logw-version' : 'lianOu',
        'x-logw-client' : 'lianOu'
    }
    url = url + St.SignatureEncryption().get_sign(payload)['Splicing'] + "&key=g90dAOmkjOljWtOr"
    response = requests.request("POST", url, headers=headers, json=payload)
    tokenInside = response.json()['data']['token']
    return tokenInside


# print(update_token_inside())
def update_token_dg() :
    """
    内部调用接口，万能token
    :return:
    """
    url = "https://testauth.lian-ou.com/auth/login/token"
    payload = {
        "userName" : "testadmin",
        "password" : "lian0u!@#2022",
        "userType" : 10
    }
    headers = {
        'Content-Type' : 'application/json',
        'x-logw-env' : 'test',
        'x-logw-version' : 'lianOu',
        'x-logw-client' : 'lianOu'
    }
    url = url + St.SignatureEncryption().get_sign(payload)['Splicing'] + "&key=g90dAOmkjOljWtOr"
    response = requests.request("POST", url, headers=headers, json=payload)
    tokenInside = response.json()['data']['token']
    return tokenInside


def UpdateToken() :
    # from http.client import HTTPConnection
    # HTTPConnection.debuglevel = 1

    # 获取内部token方法
    token_inside = update_token_inside()
    data_list = get_token_headers()
    # print(data_list)
    token_list = {}
    for l in data_list :
        app_name = l[0]  # 项目名
        token_list_upper = [ele.upper() for ele in token_list if isinstance(ele, str)]
        # 机构端的登录接口请求头比较特殊
        header = l[1]  # 请求头

        # if app_name.upper() == 'DOCGROUP':
        #     header = json.loads(header)
        #     header["uniqueid"] = "N8JyA8b5dCCWEBbD4N8GXARJ2HJmPyJ5"
        #     header["x-logw-modular"] = "hcauth"
        #     header["x-logw-env"] = "dev"

        auth_type = l[2]  # 认证方式
        request_type = l[3]  # 请求方式
        url = l[4]  # 请求url
        body = l[5]  # 请求体
        if str(auth_type) == "3" :
            token_list[l[0]] = token_inside

        elif request_type is not None and url is not None and body is not None and header is not None :
            if isinstance(body, str) :
                body = json.loads(body)
                # print(type(body))

            if str(app_name).upper() != "DAUPSE" and str(app_name).upper() != "LOCWDZ" and str(
                    app_name).upper() != "DAUPPRODUCT" :
                url = url + St.SignatureEncryption().get_sign(body)["Splicing"]
            else :
                url = url + "&" + St.SignatureEncryption().get_sign(body)["Splicing"][1 :]
                body = {}
                header = json.loads(header)
                header["x-logw-modular"] = "biadmingw"

            token_1 = Co.RequestProcessing().run_method(method=request_type, url=url, data=body, headers=header)
            # 正则获取符合的数据
            print(token_1)
            token = re.findall(r'oken":"(.+?)","', token_1)
            if len(token) == 0 :
                token = ''
            else :
                token = token[0]
            token_list[app_name] = token

            # elif str(l[2]) == "2" :
            #     Co.RequestProcessing().run_method(method=)
            #     token[l[0]] = token_inside

        else :
            print("数据异常，重新维护数据")
    # Rd.ExecuteRedis().Write_App_token(json.dumps(token_list))
    print(json.dumps(token_list))
    # print(json.loads(Rd.ExecuteRedis().Read_App_token()["data"]))
    return token_list


# print(UpdateToken())

# aaaaccc = "http://testscrm.lianouyiyuan.com/Docgroup/HaveRightsSystem?nonce=62&timestamp=1648806653&sign=8BDB92F12EEDA54D57A5E727409FA5F04129997F"
# token11111111 = re.findall(r'.com/(.+?)/', aaaaccc)
# print(token11111111)

# print(json.loads(json.dumps(ace, ensure_ascii=False).replace('这里是一个随机数', abc)))
# print(str(ace).replace('这里是一个随机数', abc))


ac_data = {"code" : 1, "msg" : "操作成功", "data" : [{"userId" : {"typee" : 2, "timee" : "0001-01-01 00:00:00"},
                                                  "operations" : [{"type" : 2, "time" : "0001-01-01 00:00:00"}]},
                                                 {"userId" : "FzIMDoctorId4300287605463040",
                                                  "operations" : [{"type" : 2, "time" : "0001-01-01 00:00:00"}]},
                                                 {"userId" : "FzIMDoctorId5095246269791280008",
                                                  "operations" : [{"type" : 2, "time" : "0001-01-01 00:00:00"}]}]}
ace = {"typee" : 9, "timee" : "ahdkahsdkhskahdhad"}
par = {"Grade" : "优先级", "parameter" : ["typee", "timee"], "req" : ["Gender", "name"]}


def data_1(parameter, data) :
    """
    parameter
    :param data:需要查找的数据原
    :param parameter:需要查找的数据列表
    :return:
    """
    data_dict = {}

    def parameterHandle(key_data, parameter_data) :
        if str(key_data) not in str(parameter_data) :
            return "不存在key"
        elif isinstance(parameter_data, dict) :
            if key_data in parameter_data.keys() :
                data_dict[key_data] = parameter_data[key_data]
            else :
                for key_data_i in parameter_data.keys() :
                    if isinstance(parameter_data[key_data_i], dict) :
                        parameterHandle(key_data, parameter_data[key_data_i])
                    elif isinstance(parameter_data[key_data_i], list) :
                        data_list = parameter_data[key_data_i][0]
                        parameterHandle(key_data, data_list)
        elif isinstance(parameter_data, list) :
            data_list = data[0]
            parameterHandle(key_data, data_list)
        else :
            print("数据有问题")
            # for data_key in data.keys():

    if isinstance(data, list) :
        for i_list in data :
            parameterHandle(i_list, parameter)
        return data_dict
    else :
        return "数据有问题"


def data_2(parameter, par_key) :
    """
    req 出参的参数处理
    :param parameter: 需要修改的请求数据
    :param par_key: 存在缓存中需要修改的数据
    :return:
    """
    data_dict = parameter

    def parameterHandle(parameter_data, key_data, cache) :
        """
        :param parameter_data:
        :param key_data:
        :param cache:
        :return:
        """
        if isinstance(parameter_data, dict) :
            if key_data in parameter_data.keys() :
                parameter_data[key_data] = cache[key_data]
            else :
                for key_data_i in parameter_data.keys() :
                    if isinstance(parameter_data[key_data_i], dict) :
                        parameterHandle(parameter_data[key_data_i], key_data, cache)
                    elif isinstance(parameter_data[key_data_i], list) :
                        for data_list in parameter_data[key_data_i] :
                            parameterHandle(data_list, key_data, cache)
        elif isinstance(parameter_data, list) :
            for data_list in parameter_data :
                parameterHandle(data_list, key_data, cache)
        else :
            print("数据有问题")

    # 判断需要修改的参数的key是否都在请求数据中
    if all(par_key_i in str(data_dict) for par_key_i in par_key.keys()) :
        for par_key_i in par_key.keys() :
            parameterHandle(data_dict, par_key_i, par_key)
        return data_dict
    else :
        return "数据有问题"


# print(type(par["parameter"]))


adf = {
    "lead" : "A",
    "contact" : {
        "A用例的id" : {
            "sex" : "sex",
            "name" : "name"
        },
        "B用例的id" : {
            "B用例对应的sex" : "sex",
            "B用例对应的name" : "name1"
        }
    }
}
qw = {"Test-123" : "123123"}
req = {"name" : "你好呀啊实打实", "sex" : "凯撒很多空间和"}

req123 = {"name1" : ["123", {"name" : "你可能饭卡手动阀了解到了警方了解到"}], "sex" : "男", "age" : "阿斯顿六十大寿看", "hei" : "加萨里的就撒了角度来解释"}


# print(adf["contact"]["B用例的id"].values())

def req_data(request, case_dict) :
    case_dict_list = []
    if isinstance(case_dict["contact"], dict) :
        for t in case_dict["contact"].keys() :
            for y in case_dict["contact"][t].values() :
                if y not in case_dict_list :
                    case_dict_list.append(y)
    else :
        return "数据有问题，重新处理用例"
    print(case_dict_list)
    if all(l in str(request) for l in case_dict_list) :
        req_dict = data_1(request, case_dict_list)
        if isinstance(case_dict["contact"], dict) and len(case_dict["contact"]) != 0 :
            allCaseDict = {}

            for i in case_dict["contact"].keys() :
                if isinstance(case_dict["contact"][i], dict) :
                    case_dict_i = {}
                    for l in case_dict["contact"][i].keys() :
                        case_dict_i[l] = req_dict[case_dict["contact"][i][l]]
                    allCaseDict[i] = case_dict_i
            return allCaseDict

    else :
        return "数据有问题，重新处理用例"


# result = Co.RequestProcessing().AssertResults(response = qweqwe, req= abcd)
# print(result)

# print(getAPhoneNumber())


# if __name__ == '__main__':
#     # print(Unicode())
#     print(GBK2312())

# from datetime import datetime
# aaa = '{"hos:8":[{"STime":"2021-12-28T09:33:00.0097316+08:00","ETime":"2021-12-28T09:33:00.0097316+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":1,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T10:55:00.0081856+08:00","ETime":"2021-12-28T11:31:00.0079557+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":552,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T11:37:01.0232167+08:00","ETime":"2021-12-28T13:49:00.0087506+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":2002,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T14:26:00.0086302+08:00","ETime":"2021-12-28T14:26:00.0086302+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":2,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T14:36:00.0075044+08:00","ETime":"2021-12-28T15:16:00.0075885+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":620,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T15:28:00.0084275+08:00","ETime":"2021-12-28T15:28:00.0084275+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":2,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T16:12:00.0078811+08:00","ETime":"2021-12-28T17:38:00.0075023+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":1297,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T18:47:00.0078515+08:00","ETime":"2021-12-28T18:47:00.0078515+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":1,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T21:33:00.0075144+08:00","ETime":"2021-12-28T21:57:00.0079127+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":380,"PassCount":0,"NoPassCount":0}],"hos:1808198464":[{"STime":"2021-12-28T09:34:00.5877352+08:00","ETime":"2021-12-28T09:35:00.009204+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":12,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T11:33:01.0078805+08:00","ETime":"2021-12-28T11:33:01.0078805+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":12,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T11:39:02.0232606+08:00","ETime":"2021-12-28T11:39:02.0232606+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":12,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T13:50:00.0084223+08:00","ETime":"2021-12-28T13:50:00.0084223+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":12,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T15:18:00.0076229+08:00","ETime":"2021-12-28T15:18:00.0076229+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":24,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T18:17:00.0075567+08:00","ETime":"2021-12-28T18:19:00.0075715+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":463,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T18:48:00.0079155+08:00","ETime":"2021-12-28T18:49:00.0078543+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":3132,"PassCount":0,"NoPassCount":0},{"STime":"2021-12-28T18:52:00.0087264+08:00","ETime":"2021-12-28T19:14:00.0079474+08:00","STimeStr":null,"ETimeStr":null,"HeartCount":7296,"PassCount":0,"NoPassCount":0}]}'
# aaaa = json.loads(aaa)
#
# for i in aaaa.keys():
#     a_mub = len(aaaa[i])
#     for l in range(0, a_mub):
#         # print(aaaa[i][l]["STime"][:19])
#         # print(datetime.strptime(aaaa[i][l]["STime"][:19], "%Y-%m-%dT%H:%M:%S"))
#         STime = datetime.strptime(aaaa[i][l]["STime"][:19], "%Y-%m-%dT%H:%M:%S")
#         ETime = datetime.strptime(aaaa[i][l]["ETime"][:19], "%Y-%m-%dT%H:%M:%S")
#         # print(aaaa[i][l]["STime"])
#         # print(aaaa[i][l]["ETime"])
#         aaaa[i][l]["STime"] = str(STime)
#         aaaa[i][l]["ETime"] = str(ETime)

# print(json.dumps(aaaa))


# if '9' == "9" :
#     count_loop = 0
#     ab = 1
#     while  count_loop < 10 :
#         ab += 10
#         count_loop += 1
#         print(count_loop)
#         print(ab)

# Relate = {
#             "level" : "关联用例等级",
#             "contact" : {
#                 "关联用例id" : {
#                     "inq（关联用例的参数）" : "inq（接口返回的参数）",
#                     "docName（关联用例的参数）" : "docName（接口返回的参数）"
#                 }
#             }
#         }
#
# # Relate = str(Relate)
# Relate = json.dumps(Relate,ensure_ascii=False)
# sql_url_change = "insert into api_case SELECT case_seq, A.api_id, A.app_name,A.api_type,A.request_type,A.api_name,A.api_host,A.api_path,A.parameter,A.response,'1' Ischange,'1' IsRead,A.auth_type, actual_value, %s info_Relate FROM  api_info A LEFT JOIN api_case B ON A.api_id = B.api_id WHERE B.api_id IS NULL;"
# # self.cursor.execute(sql_url_change, (Relate,))
# # print(sql_url_change)
# # print(sql_url_change, Relate)
# print(Relate)


#     def get_token_headers1111(self) :
#         """
#         获取项目信息
#         :return:
#         """
#         sql = "SELECT case_seq, api_path FROM `api_case` WHERE app_name = 'scrm'  AND Ischange = '0'  AND IsRead = '1' ; "
#         self.cursor.execute(sql)
#         ab = self.cursor.fetchall()
#         return ab
#
#     def get_token_headers2222(self, aa, bb) :
#         """
#         获取项目信息
#         :return:
#         """
#         sql = "SELECT api_id FROM `api_case` WHERE app_name = 'LoScrm' and api_path = %s "
#         self.cursor.execute(sql, bb)
#         ab = self.cursor.fetchall()
#         print(aa)
#         if ab == () :
#             print(ab)
#             sql = "UPDATE api_case SET Ischange = '1' , IsRead = '0' WHERE case_seq = %s"
#             self.cursor.execute(sql, aa)
#             self.db.commit()
#         else:
#             path = ab[0][0]
#             sql = "UPDATE api_case SET api_id = %s , app_name = 'LoScrm' WHERE case_seq = %s"
#             self.cursor.execute(sql, (path, aa))
#             self.db.commit()
#         return
#
#
# ABC = ExecuteBusiness().get_token_headers1111()
# for i in ABC :
#     ExecuteBusiness().get_token_headers2222(i[0], i[1])


# 同步数据用
# def get_token_headers1111(self) :
#     """
#     获取项目信息
#     :return:
#     """
#     sql = "SELECT case_seq, api_id FROM `api_case` "
#     self.cursor.execute(sql)
#     ab = self.cursor.fetchall()
#     return ab
#
# def get_token_headers2222(self, case, api_id) :
#     """
#     获取项目信息
#     :return:
#     """
#     sql = "SELECT remarks FROM `api_info` WHERE api_id = %s "
#     self.cursor.execute(sql, api_id)
#     ab = self.cursor.fetchall()
#     # print(ab[0][0])
#     if ab == () :
#         print(ab)
#         # sql = "UPDATE api_case SET Ischange = '1' , IsRead = '0' WHERE case_seq = %s"
#         # self.cursor.execute(sql, aa)
#         # self.db.commit()
#     else:
#         path = ab[0][0]
#         sql = "UPDATE api_case SET remarks = %s WHERE case_seq = %s"
#         self.cursor.execute(sql, (path, case))
#         self.db.commit()
#     return


# ABC = ExecuteBusiness().get_token_headers1111()
# for i in ABC :
#     # print(i)
#     ExecuteBusiness().get_token_headers2222(i[0], i[1])

# print("DaupProduct".upper())
#
# for l in [1]:
#     print("111")
#     print("111")

def decide_result(response_data, req_data) :
    if isinstance(response_data, dict) :
        if not isinstance(response_data, dict) :
            return False
        else :
            for abc in response_data.keys() :
                if abc not in req_data.keys() :
                    return False
                else :
                    decide_result(response_data[abc], req_data[abc])

    if isinstance(response_data, list) :
        if not isinstance(req_data, list) :
            return False
        else :
            count_nub = 0
            for response_data_list in response_data :
                if isinstance(response_data_list, str) :
                    count_all = 0
                    for reg_data_list in req_data :
                        if isinstance(response_data_list, str) :
                            if str(response_data_list) == str(reg_data_list) :
                                count_all += 1
                    if len(response_data_list) == count_all :
                        count_nub += 1

                else :
                    for reg_data_list in req_data :
                        decide_result(response_data_list, reg_data_list)
    else :
        if str(response_data) != str(req_data) :
            return False

    return True


#
# token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
# Co.SubmitInq().NoPass(token)


import requests

# url = "http://testgw.lianou.com/api/Project/ImportProjectPromotion?timestamp=1&nonce=1&sign=1"
#
# payload = {}
# files = [
#     ('file', ('123.xlsx', open('C:/Users/Dell/Desktop/123.xlsx', 'rb'),
#               'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
# ]
# headers = {}

# response = requests.request("POST", url, headers=headers, data=payload, files=files)
#
# print(response.text)

# parameter_data = [
#     {"file1" : "C:/Users/Dell/Desktop/123.xlsx"},
#     {"file2" : "C:/Users/Dell/Desktop/123.xlsx"}
#
# ]
# a1 = list(aaaaa[0].keys())
# print(a1[0])
# parameter_data_list = []
# for i in parameter_data :
#     data_key = list(i.keys())[0]
#     data_value = i[data_key]
#     file_1 = ('data_key',
#               ('123.xlsx', open(data_value, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
#     parameter_data_list.append(file_1)
#
# print(parameter_data_list)


# session.request(method, url, **kwargs)

# response = requests.session().r("POST", url, headers=headers, data=payload, files=parameter_data_list)


# qqqq = {
# 	"file": [{
# 		"file": "C:/Users/Dell/Desktop/项目赠品投入明细导入模版.xlsx"
# 	}],
# 	"data": {}
# }
# file_name, file_extension = os.path.splitext("C:/Users/Dell/Desktop/项目赠品投入明细导入模版.xlsx")
#
# print(file_extension)

# token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
# Co.SubmitInq().NoPass(token)


# Co.SubmitInq().save_workOrder()
