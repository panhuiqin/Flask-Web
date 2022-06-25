# -*-coding: utf-8 -*-
# import method.BusinessLayer as Db_execute
import os
import pathlib
import time
import requests
# import CommonMethod.ReadConfig as Rf
import CommonMethod.Signature as St
import method.BusinessLayer as Bl
import method.RedisOperation as Ro
import method.RedisOperation as Rd
# import CommonMethod.LogOutput as LogInfo
import json
import re
import random
import datetime

# 接口请求操作
# 控制token过期死循环
count = 0


class DataProcessing :
    @classmethod
    def GetData(cls, parameter, data) :
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

    @classmethod
    def ModifyData(cls, parameter, par_key) :
        """
        获取缓存的数据，修改请求的入参
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

                        elif isinstance(parameter_data[key_data_i], str) :
                            try :
                                parameter_data_data = json.loads(parameter_data[key_data_i])
                                abc = parameterHandle(parameter_data_data, key_data, cache)
                                parameter_data[key_data_i] = json.dumps(abc)
                            except :
                                continue

            elif isinstance(parameter_data, list) :
                for data_list in parameter_data :
                    parameterHandle(data_list, key_data, cache)
            return parameter_data

        # 判断需要修改的参数的key是否都在请求数据中
        # if all(par_key_i in str(data_dict) for par_key_i in par_key.keys()) :
        for par_key_i in par_key.keys() :
            parameterHandle(data_dict, par_key_i, par_key)
        return data_dict

        # else:
        #     return "数据有问题"

    @classmethod
    def req_data(cls, request, case_dict) :
        """
        处理数据，生成需要用到的缓存数据
        :param request:
        :param case_dict:
        :return:
        """
        req_data = json.loads(Rd.ExecuteRedis().Read_App_data()["data"])
        # print(case_dict)
        # case_dict = json.loads(case_dict)
        case_dict_list = []
        all_case_dict = {}
        if isinstance(case_dict["contact"], dict) :
            for t in case_dict["contact"].keys() :
                for y in case_dict["contact"][t].values() :
                    if y not in case_dict_list :
                        case_dict_list.append(y)
        else :
            print("数据有问题，重新处理用例")
        # print(case_dict_list)
        if all(l in str(request) for l in case_dict_list) :
            req_dict = DataProcessing().GetData(request, case_dict_list)
            if isinstance(case_dict["contact"], dict) and len(case_dict["contact"]) != 0 :
                for i in case_dict["contact"].keys() :
                    if isinstance(case_dict["contact"][i], dict) :
                        case_dict_i = {}
                        for l in case_dict["contact"][i].keys() :
                            case_dict_i[l] = req_dict[case_dict["contact"][i][l]]
                        all_case_dict[i] = case_dict_i


        else :
            print("数据有问题，重新处理用例")
        # 跟新数据到rides
        for case_i_key in all_case_dict.keys() :
            if case_i_key in req_data.keys() :
                for case_i_data_key in all_case_dict[case_i_key].keys() :
                    req_data[case_i_key][case_i_data_key] = all_case_dict[case_i_key][case_i_data_key]

            elif case_i_key not in req_data.keys() :
                req_data[case_i_key] = all_case_dict[case_i_key]

        Rd.ExecuteRedis().Write_App_data(json.dumps(req_data, ensure_ascii=False))


class SubmitInq :

    def __init__(self, token=None) :
        if token is None :
            self.open_token = "A3763990665E4C268AFFC77BF687EA11BAB960ACE08167885A8494CD2117B7CF"
        else :
            self.open_token = token
        self.token = "token"
        self.AccessToken_doctor = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjE1NjIyMTIwMjI5Iiwic3ViIjoiNDk4NTExNjg5Mjc1NDI1MzU3MCIsInNjb3BlIjoiIiwiZXh0IjoiIiwicm9sZSI6IkRvY3RlciIsImp0aSI6IjZjYWY2YzA0LWM3ZGEtNDUxMS05ODQwLTIzN2M4MzM3M2RmZiIsImlhdCI6IjA5LzEwLzIwMjEgMTA6MjA6NTUiLCJleHAiOjE2MzEyNzI4NTUsIm5iZiI6MTYzMTI2OTA3NSwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxpYW4tb3UuY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRoLmxpYW4tb3UuY29tLzEvMSJ9.Ro_Bn_-uyar1xIBmUtzIK7EXC7aFoH1GhD-_T__zVh0'
        self.RefreshToken = '279ba636-4669-458b-a991-4a6814f4bc8f'
        self.InquiryId = '4301546356116224'  # 问诊id
        self.Desc = '测试拒方理由'  # 拒方理由
        self.env = 'test'
        self.modular = 'open'  # appservice
        self.version = '2.0'

    def get_open_token(self, AppKey, AppSecret) :
        """
        复诊医生端拒绝开方接口: SaveVisitPrescribing
        :return:
        """
        url = "https://testgw.lianouyiyuan.com//LianOuService/QueryToken/"
        payload = {
            'appKey' : AppKey,
            'appSecret' : AppSecret
        }
        headers = {
            'Content-Type' : 'application/json',
            'x-logw-modular' : self.modular,
            'x-logw-client' : 'third',
            'x-logw-version' : self.version,
            'x-logw-env' : self.env
        }
        url = url + (St.SignatureEncryption().get_sign(payload))["Splicing"]
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        self.open_token = response.json()["data"]["token"]
        return self.open_token

    def save_open(self, AppKey) :
        """
        复诊医生端拒绝开方接口: SaveVisitPrescribing
        :parameter AppKey
        :return: 京东到家
        """
        inq = random.randint(1000000, 99999999)
        channel = {
            "3303788178" : "BC4FCAD6BE44E6944BD3354308777A5B6594EF3BB09777FB2E57E630EE53470C",  # 京东到家
            "3304011076721800" : "cc86da165a87433b85b823758c4f81b81C5E0466813075CEB9A087AE588A984F",  # 健康锦囊
            "3307039107" : "7B7CFE1766AD4EABB852AB66069AEE9D989DDDDD84FD94D373845A2E324B276A",  # 药房网商城
            "3302069692" : "e2eec9263bb04cb4a65301267b945e6fFFD042007BD24948A3112364C7DEDB85",  # 德开
            "3303113591" : "1d03e7864d124d5aa336acbd3d809573BDFE6F4AAD8CB9B1C148208540B13370",  # 饿了么
            "123456" : "F523ED38DA894ACD86F21B3E7B37224BF2A76D9733CD3C31882A2031A52A5",  # 莲藕app
            "3304011597765134" : "c6674da373784d22ac2f94944b986b9050BF55BB6DCFFCE1059FE604676C21C4",  # 小荷健康
            "3304014281255993" : "920d009599d44ee1b45e1355a3f7895aF9BA56A76A8EEA6C9F243A582E4B3B35",  # 百度
            "3304013515861185" : "eaf927ee24fd473891eed6ce5ddeaa83CB120B3282BBE6C167D86EE1CFFBD05E",  # 京东健康
            "3304013388910009" : "b7b528559e52482a85f3aaa35da1949612D6CBD661E5341020EF2F6C34C53568",  # 快手渠道
            "3304014277455426" : "b9c08f9441654f05a630db717cb7d6ea84DD9657EB88146AB9FC24317D98D62B",  # 药联
            "330401355994966" : "e79fa8782c89429cab82318b6a533716A54AC1E086BDFDB340302D342410025F",  # 新华大药店
            "3304013717704488" : "cfbce208af6e4ad7b546fbd74caca041765962D008396E3BA68D214FEF69ED0D"  # 药联
        }
        url = "https://testgw.lianouyiyuan.com/LianOuService/SaveInquiry"
        payload = {'AppKey' : AppKey, 'Token' : self.open_token, 'UserId' : 32, 'OutOrderId' : inq, 'InquiryId' : "",
                   'Status' : 0,
                   'Name' : "陈他庆", 'IDCard' : "12345681966", 'Birthdate' : "1993-09-07", 'Sex' : 1,
                   'PhoneNo' : "13245699875",
                   'PMHType' : 0, 'AMHType' : 0, 'FMHType' : 0, 'LiverType' : 0, 'RenalType' : 0, 'NurseType' : 0,
                   'PMH' : "感冒",
                   'AMH' : "花粉过敏", 'FMH' : "家族病史", 'LiverDesc' : "肝脏异常", 'RenalDesc' : "肾脏异常", 'NurseDesc' : "怀孕中",
                   'Description' : "最近感冒，发烧", 'CompanyId' : "1235654", 'CompanyName' : "泰阳大药房", 'Weight' : 50,
                   'ModeType' : 1,
                   'DiseaseInfos' : "[{\"DiseaseId\":1203,\"DiseaseName\":\"冠心病\"}]",
                   'DrugsInfos' : "[{\"DrugName\":\"柏子养心丸\",\"CommonName\":\"柏子养心丸\",\"Spec\":\"36g*1瓶\\/盒\",\"ApprovalNO\":\"国药准字H20143255\",\"Producer\":\"葵花药业集团湖北武当有限公司\",\"Count\":1,\"CountUnit\":\"盒\"}]",
                   'PicInfos' : "",
                   # "CNCode": "A10210",
                   # "CNDrugsName": "五味子",
                   "DoctorId" : "4985116892754253570",
                   "DoctorName" : "吴伟谦",
                   }
        headers = {
            'Content-Type' : 'application/json',
            'x-logw-modular' : self.modular,
            'x-logw-client' : 'third',
            'x-logw-version' : self.version,
            'x-logw-env' : self.env
        }
        url = url + (St.SignatureEncryption().get_sign(payload))["Splicing"]
        # r_sign = '{0}?{1}={2}&{3}={4}&{5}={6}'.format(url, 'nonce', autograph["nonce"], 'timestamp',
        #                                               autograph["timestamp"],
        #                                               'sign', autograph["sign"])
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        req1 = response.json()
        if str(req1["code"]) == '4002' :  # and str(response.json()["msg"]) == 'Token过期':
            token = SubmitInq().get_open_token(AppKey=AppKey, AppSecret=channel[AppKey])
            req1 = SubmitInq(token).save_open(AppKey)
            return req1
        print("问诊号：" + str(inq))
        return req1

    @classmethod
    def save_workOrder(cls) :
        token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
        url = "https://gw.lian-ou.com/Extend/ReleaseInquiry"
        payload = {
            "Communicate" : "[{\"content\":\"[患者]吴咏年/女/44岁\\n[疾病]高血压\\n[肝功能]正常\\n[肾功能]正常\\n[是否备孕/怀孕/哺乳期]否\\n[过敏史]无\\n[其他病史]无\\n[家族病史]无\",\"role\":\"other\",\"type\":1,\"ts\":1649835594},{\"content\":\"确认已使用过此次预订的药品\",\"role\":\"other\",\"type\":1,\"ts\":1649835594},{\"content\":\"您好，我是医师解晓谜，已收到您的问诊信息，请稍等，正在根据您的信息进行诊断\",\"role\":\"doctor\",\"type\":1,\"ts\":1649835594},{\"content\":\"收到您的复诊申请：已看到您填写使用过该药品治疗该疾病，您本人使用过程没有出现过敏、不良反应且目前病情平稳是吧。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649835614},{\"content\":\"收到您的复诊申请：已看到您填写使用过该药品治疗该疾病，您本人使用过程没有出现过敏、不良反应且目前病情平稳是吧。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649841444},{\"content\":\"收到您的复诊申请：已看到您填写使用过该药品治疗该疾病，您本人使用过程没有出现过敏、不良反应且目前病情平稳是吧。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649985615},{\"content\":\"【shift+c】请问还有什么要问的吗？\",\"role\":\"doctor\",\"type\":1,\"ts\":1649994931}]",
            "inq" : "{\"Name\":\"吴咏年\",\"Birthdate\":\"\",\"Sex\":2,\"PhoneNo\":\"13162443361转0129\",\"Province\":\"\",\"City\":\"\",\"AMHType\":\"0\",\"AMH\":\"\",\"FMHType\":\"0\",\"FMH\":\"\",\"PMHType\":\"0\",\"PMH\":\"\",\"RenalType\":\"0\",\"RenalDesc\":\"正常\",\"LiverType\":\"0\",\"LiverDesc\":\"\",\"NurseType\":\"0\",\"NurseDesc\":\"否\",\"History\":\"\",\"CompanyName\":\"美团商家\",\"OutOrderId\":\"1514146339615850559\",\"SymptomDesc\":\"高血压\",\"Complain\":\"高血压\",\"PicUrls\":\"\",\"DoctorName\":\"LR584\",\"nickName\":\"xbg951765101\",\"ConfirmedDisease\":\"高血压\",\"isId\":\"4660819029381888\"}",
            "disList" : "[{\"Name\":\"高血压\",\"id\":1}]",
            "drugs" : "[{\"Title\":\"[兰迪]苯磺酸氨氯地平片5mg*28片/盒\",\"ComName\":\"苯磺酸氨氯地平片\",\"DrugsId\":\"\",\"Usage\":\"口服\",\"Specs\":\"5mg*28片/盒\",\"Remark\":\"\",\"FrequencyValue\":\"一日\",\"FrequencyUnit\":\"1次\",\"Frequency\":\"一日1次\",\"DoseValue\":\"5\",\"DoseUnit\":\"毫克\",\"Days\":\"1\",\"Count\":\"2\",\"Unit\":\"件\"}]",
            "appName" : "美团插件合理用药检测",
            "age" : "44岁",
            "inShop" : "美团商家",
            "userName" : "LR584",
            "ver" : "4.4.5",
            "plugName" : "美团开方",
            "creater" : "美团",
            "appCode" : "103",
            "HasCalled" : "false",
            "doctorId" : "109521577",
            "hospitalName" : "莲藕互联网医院",
            "appKey" : "330245103001",
            "nickName" : "xbg951765101",
            "tags" : "",
            "pass" : "[{\"Id\":156,\"Type\":1,\"Name\":\"DiagNeedConfirm\",\"Title\":\"包含需再次确认诊断\",\"Msg\":\"诊断【高血压】需与用户确认，是否已在线下就诊\",\"Suggest\":\"如用户不同意用此诊断，请修改诊断\",\"Tip\":\"\",\"Objection\":\"\",\"MTObjection\":\"\",\"MTObjectionSelect\":\"其他\",\"OTagId\":null,\"OTagName\":null,\"InqWords\":\"\",\"ReqPassMode\":1,\"ReqPassInqWords\":\"无\",\"SendMsg\":\"\",\"Color\":\"red\",\"Keywords\":[]},{\"Id\":90,\"Type\":2,\"Name\":\"DidNotSpeak\",\"Title\":\"患者从未回复不得开方\",\"Msg\":\"患者没有作任何回复，无对话不得开方\",\"Suggest\":\"不得开方\",\"Tip\":\"\",\"Objection\":\"\",\"MTObjection\":\"\",\"MTObjectionSelect\":\"其他\",\"OTagId\":null,\"OTagName\":null,\"InqWords\":\"\",\"ReqPassMode\":1,\"ReqPassInqWords\":\"无\",\"SendMsg\":\"\",\"Color\":\"red\",\"Keywords\":[]}]",
            "Account" : "15622120229"
        }
        payload1 = {
            "Communicate" : "[{\"content\":\"[患者]郑玉莉/女/55岁\\n[疾病]慢性浅表性胃炎\\n[肝功能]正常\\n[肾功能]正常\\n[是否备孕/怀孕/哺乳期]否\\n[过敏史]无\\n[其他病史]无\\n[家族病史]无\",\"role\":\"other\",\"type\":1,\"ts\":1649488491},{\"content\":\"确认已使用过此次预订的药品\",\"role\":\"other\",\"type\":1,\"ts\":1649488491},{\"content\":\"您好，我是医师解晓谜，已收到您的问诊信息，请稍等，正在根据您的信息进行诊断\",\"role\":\"doctor\",\"type\":1,\"ts\":1649488491},{\"content\":\"收到您的复诊申请：已看到您填写使用过该药品治疗该疾病，您本人使用过程没有出现过敏、不良反应且目前病情平稳是吧。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649488490},{\"content\":\"线上复诊开方，适用线下已确诊疾病、已用过问诊的药品且无不良反应。我根据您提交的复诊信息进行分析判断，现在为您开具处方，请严格按照原处方和药品说明书用法用量使用。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649488501},{\"content\":\"【莲藕医生提醒您】1、胃炎应注意按时规律进食，避免暴饮暴食和食用刺激性食物。2、猴头菌片用药期间饮食宜清淡，避免辛辣、生冷、油腻食物。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649488502},{\"content\":\"https://p0.meituan.net/prescription/a1aa41fc03ac5febcab1ac8266b7cf9854935.png?token=1.1652080507.rjjfd4svhvj9bvgf000000000066a67c.47534c44cd7e37974f66e6a3114e6e45\",\"role\":\"doctor\",\"type\":2,\"ts\":1649488507},{\"content\":\"已为您开具处方，请遵医嘱使用，1、猴头菌片，口服，每次3片，一日3次。考虑用药安全：1、请您再次确认用过该药品且无不良反应。如未用过请取消订单；2、应严格按原处方和《药品说明书》使用（严格对照用法用量、不良反应、禁忌、注意事项和药物相互作用）。3、如病情发生变化，或用药期间如有不适，请立即停药并及时到当地医院就诊。稍后会话将关闭，如有疑虑请在会话关闭前提出。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649488504},{\"content\":\"如病情发生变化，请及时到当地医院就诊。稍后会话将关闭，如有疑虑请在会话关闭前提出。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649742839},{\"content\":\"如病情发生变化，请及时到当地医院就诊。稍后会话将关闭，如有疑虑请在会话关闭前提出。\",\"role\":\"doctor\",\"type\":1,\"ts\":1649836284},{\"content\":\"收到您的复诊申请：已看到您填写使用过该药品治疗该疾病，您本人使用过程没有出现过敏、不良反应且目前病情平稳是吧。\",\"role\":\"doctor\",\"type\":1,\"ts\":1650436038}]",
            "inq" : "{\"Name\":\"郑玉莉\",\"Birthdate\":\"\",\"Sex\":2,\"PhoneNo\":\"\",\"Province\":\"\",\"City\":\"\",\"AMHType\":\"0\",\"AMH\":\"\",\"FMHType\":\"0\",\"FMH\":\"\",\"PMHType\":\"0\",\"PMH\":\"\",\"RenalType\":\"0\",\"RenalDesc\":\"正常\",\"LiverType\":\"0\",\"LiverDesc\":\"\",\"NurseType\":\"0\",\"NurseDesc\":\"否\",\"History\":\"\",\"CompanyName\":\"美团商家\",\"OutOrderId\":\"1512690484026417226\",\"SymptomDesc\":\"慢性浅表性胃炎\",\"Complain\":\"慢性浅表性胃炎\",\"PicUrls\":\"\",\"DoctorName\":\"LR584\",\"nickName\":\"zJE378044597\",\"ConfirmedDisease\":\"慢性浅表性胃炎\",\"isId\":\"4668198780883712\"}",
            "disList" : "[{\"Name\":\"慢性浅表性胃炎\",\"id\":1}]",
            "drugs" : "[{\"Title\":\"[云鹏]猴头菌片0.25g*100片/瓶/盒\",\"ComName\":\"猴头菌片\",\"DrugsId\":\"\",\"Usage\":\"口服\",\"Specs\":\"0.25g*100片/瓶/盒\",\"Remark\":\"\",\"FrequencyValue\":\"一日\",\"FrequencyUnit\":\"3次\",\"Frequency\":\"一日3次\",\"DoseValue\":\"3\",\"DoseUnit\":\"片\",\"Days\":\"1\",\"Count\":\"6\",\"Unit\":\"件\"}]",
            "appName" : "美团插件合理用药检测",
            "age" : "55岁",
            "inShop" : "美团商家",
            "userName" : "LR584",
            "ver" : "4.4.5",
            "plugName" : "美团开方",
            "creater" : "美团",
            "appCode" : "103",
            "HasCalled" : "false",
            "doctorId" : "109521577",
            "hospitalName" : "莲藕互联网医院",
            "appKey" : "330245103001",
            "nickName" : "zJE378044597",
            "tags" : "",
            "pass" : "[{\"Id\":90,\"Type\":2,\"Name\":\"DidNotSpeak\",\"Title\":\"患者从未回复不得开方\",\"Msg\":\"患者没有作任何回复，无对话不得开方\",\"Suggest\":\"不得开方\",\"Tip\":\"\",\"Objection\":\"\",\"MTObjection\":\"\",\"MTObjectionSelect\":\"其他\",\"OTagId\":null,\"OTagName\":null,\"InqWords\":\"\",\"ReqPassMode\":1,\"ReqPassInqWords\":\"无\",\"SendMsg\":\"\",\"Color\":\"red\",\"Keywords\":[]}]",
            "Account" : "15622120229"
        }
        headers = {
            'x-logw-modular' : 'workorder',
            'x-logw-version' : '4.4.5',
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'x-logw-env' : 'test',
            'authorization' : 'Bearer ' + token['workorder'],
            'plug' : 'mt',
            'x-logw-client' : 'mt'
        }
        url1 = url + (St.SignatureEncryption().get_sign(payload))["Splicing"]
        url2 = url + (St.SignatureEncryption().get_sign(payload1))["Splicing"]
        response = RequestProcessing().run_method(method='POST', url=url1, data=payload, headers=headers)
        response1 = RequestProcessing().run_method(method='POST', url=url2, data=payload1, headers=headers)
        print(response)
        print(response1)
        # print(response1)

    @classmethod
    def Get_Inq_doctor(cls, token) :
        heard = {"x-logw-modular" : "fzdoc", "x-logw-version" : "2.0", "Content-Type" : "application/json",
                 "Accept" : "application/json", 'authorization' : 'Bearer ' + token['fzdoctor']}
        parameter = {"ReceiveStatus" : 1}
        url = 'https://testgw.lianouyiyuan.com/api/DocOrder/GetDocInquiry'
        url = url + (St.SignatureEncryption().get_sign(parameter))["Splicing"]
        reqs = RequestProcessing().run_method(method='POST', url=url, data=parameter,
                                              headers=heard)
        return reqs

    @classmethod
    def NoPass_doctor(cls, inq, token) :
        heard = {"x-logw-modular" : "fzdoc", "x-logw-version" : "2.0", "Content-Type" : "application/json",
                 "Accept" : "application/json", 'authorization' : 'Bearer ' + token['fzdoctor']}
        parameter = {"Desc" : "6岁以下儿童开电子处方需要监护人和专业医生在现场，为了用药安全，不能为你开具处方", "InquiryId" : inq, "RejectId" : 2}
        url = 'https://testgw.lianouyiyuan.com/api/DocOrder/NoPass'
        url = url + (St.SignatureEncryption().get_sign(parameter))["Splicing"]
        RequestProcessing().run_method(method='POST', url=url, data=parameter,
                                       headers=heard)

    # @classmethod
    # def Get_Inq_hosptial(cls, token) :
    #     heard = {"x-logw-modular" : "fzhosp", "x-logw-version" : "2.0", "Content-Type" : "application/json",
    #              "Accept" : "application/json", 'authorization' : 'Bearer ' + token['hosptial']}
    #     parameter = {"AppKey":"0","InquiryId":""}
    #     url = 'https://testgw.lianouyiyuan.com/api/Pharmacist/GetInquiry'
    #     url = url + (St.SignatureEncryption().get_sign(parameter))["Splicing"]
    #     reqs = RequestProcessing().run_method(method='POST', url=url, data=parameter,
    #                                           headers=heard)
    #     return reqs
    #
    # @classmethod
    # def NoPass_hosptial(cls, inq, token) :
    #     heard = {"x-logw-modular" : "fzdoc", "x-logw-version" : "2.0", "Content-Type" : "application/json",
    #              "Accept" : "application/json", 'authorization' : 'Bearer ' + token['fzdoctor']}
    #     parameter = {"Desc" : "6岁以下儿童开电子处方需要监护人和专业医生在现场，为了用药安全，不能为你开具处方", "InquiryId" : inq, "RejectId" : 2}
    #     url = 'https://testgw.lianouyiyuan.com/api/Pharmacist/NoPass'
    #     url = url + (St.SignatureEncryption().get_sign(parameter))["Splicing"]
    #     RequestProcessing().run_method(method='POST', url=url, data=parameter,
    #                                    headers=heard)

    @classmethod
    def NoPass(cls, token) :
        mub = 0
        while mub < 5 :
            list_s = SubmitInq().Get_Inq_doctor(token)
            for l in json.loads(list_s)['data'] :
                l_inq = l['InquiryId']
                SubmitInq().NoPass_doctor(l_inq, token)
            time.sleep(2)
            mub += 1

        # 药师
        # mub1 = 0
        # while mub1 < 5 :
        #     list_s = SubmitInq().Get_Inq_doctor(token)
        #     for l in json.loads(list_s)['data'] :
        #         l_inq = l['InquiryId']
        #         SubmitInq().NoPass_doctor(l_inq, token)
        #     time.sleep(2)
        #     mub1 += 1


class RequestProcessing :
    @classmethod
    def AssertResults(cls, response, req) :
        """
        判断断言函数
        :param response:
        :param req:
        :return:
        """
        # def decide_result(response_data, req_data) :
        #     """
        #     判断断言递归方法
        #     :param response_data:
        #     :param req_data:
        #     :return:
        #     """
        #     if isinstance(response_data, dict) :
        #         if not isinstance(req_data, dict) :
        #             return False
        #         else:
        #             for abc in response_data.keys():
        #                 if abc not in req_data.keys():
        #                     return False
        #                 else:
        #                     decide_result(response_data[abc], req_data[abc])
        #
        #     if isinstance(response_data, list) :
        #         if not isinstance(req_data, list) :
        #             return False
        #         else :
        #             count_nub = 0
        #             for response_data_list in response_data :
        #                 if isinstance(response_data_list, str) :
        #                     count_all = 0
        #                     for reg_data_list in req_data :
        #                         if isinstance(response_data_list, str) :
        #                             if str(response_data_list) == str(reg_data_list) :
        #                                 count_all += 1
        #                     if len(response_data_list) == count_all :
        #                         count_nub += 1
        #
        #                 else :
        #                     for reg_data_list in req_data :
        #                         decide_result(response_data_list, reg_data_list)
        #
        #     else :
        #         if str(response_data) != str(req_data):
        #             return False
        #
        #     return True
        #
        # # return decide_result(response, req)
        #
        # if isinstance(response, str) :
        #     response = response.replace('None', 'null')
        #     try :
        #         response = json.loads(response)
        #     except :
        #         print("断言数据正确，需要修数据")
        #         return False
        # if isinstance(req, str) :
        #     req = req.replace('None', 'null')
        #     try :
        #         req = json.loads(req)
        #     except :
        #         print("接口放回数据不是json结构")
        #         return False
        # # 判断key是否都存在返回的参数中
        # if isinstance(req, dict) and isinstance(response, dict):
        #     return decide_result(response, req)
        # else :
        #     print("数据不是json结构")
        #     return False

        # print(req)
        # print(response)
        if isinstance(response, str) :
            response = response.replace('None', 'null')
            try :
                response = json.loads(response)
            except :
                print("断言数据正确，需要修数据")
                return False
        if isinstance(req, str) :
            req = req.replace('None', 'null')
            try :
                req = json.loads(req)
            except :
                # print("接口放回数据不是json结构")
                # return False
                pass

        # 判断key是否都存在返回的参数中
        if isinstance(response, dict) :
            if isinstance(req, dict) and isinstance(response, dict) :
                for i in response.keys() :
                    if i not in req.keys() :
                        return False
                    # 判断value是否和返回的参数一样
                    elif i in req.keys() :
                        # 判断返回值是字符串，结果是否相等
                        if isinstance(response[i], str) :
                            if not isinstance(req[i], (str, int)) :
                                return False
                            else :
                                if str(response[i]) != str(req[i]) :
                                    return False

                        # 判断返回值是字典，结果是否相等
                        elif isinstance(response[i], dict) :
                            if not isinstance(req[i], dict) :
                                return False
                            else :
                                for n in response[i].keys() :
                                    # 用例的key不存在返回值的key中，输出false
                                    if n not in req[i].keys() :
                                        return False

                                    # 用例的key存在返回值的key中
                                    else :
                                        # 返回值是字典
                                        if isinstance(response[i][n], dict) :
                                            if not isinstance(req[i][n], dict) :
                                                return False

                                            # 用例的key存在返回值的key中
                                            else :
                                                for j in response[i][n].keys() :
                                                    if j not in req[i][n].keys() :
                                                        return False

                                                    # 用例的key存在返回值的key中
                                                    else :
                                                        if isinstance(response[i][n][j], list) :
                                                            for g in response[i][n][j] :
                                                                if isinstance(g, str) :
                                                                    if g not in response[i][n][j] :
                                                                        return False
                                                                if isinstance(g, dict) :
                                                                    if not isinstance(req[i][n][j][g], dict) :
                                                                        return False
                                                                    else :
                                                                        for jn in response[i][n][j][g].keys() :
                                                                            if jn not in req[i][n][j][g].keys() :
                                                                                return False
                                                                            else :
                                                                                if str(response[i][n][g][j][jn]) != str(
                                                                                        req[i][n][g][j][jn]) :
                                                                                    return False

                                                        elif isinstance(response[i][n][j], dict) :
                                                            if isinstance(req[i][n][j], dict) :
                                                                return False
                                                            else :
                                                                for jn in response[i][n][j].keys() :
                                                                    if isinstance(response[i][n][j][jn], dict) :
                                                                        for jnq in response[i][n][j][jn].keys() :
                                                                            if jnq not in req[i][n][j][jnq].keys() :
                                                                                return False
                                                                            else :
                                                                                if str(response[i][n][j][jnq][jnq]) != str(
                                                                                        req[i][n][j][jnq][jnq]) :
                                                                                    return False

                                                                    elif isinstance(response[i][n][j][jn], list) :
                                                                        for je in response[i][n][j][jn] :
                                                                            if je not in req[i][n][j][jn] :
                                                                                return False
                                                                    else :
                                                                        if str(response[i][n][j][jn]) != str(
                                                                                req[i][n][j][jn]) :
                                                                            return False

                                                        else :
                                                            if str(response[i][n][j]) not in str(req[i][n][j]) :
                                                                return False

                                        # 返回的数据是list
                                        elif isinstance(response[i][n], list) :
                                            if not isinstance(req[i][n], list) :
                                                return False
                                            else :
                                                # 取列表的数据，判断列表内容是否在返回值中
                                                s = 0
                                                for h in response[i][n] :
                                                    # 列表的下一级是字典的情况
                                                    if isinstance(h, dict) :
                                                        for f in req[i][n] :
                                                            # 都是字典的条件下
                                                            if isinstance(f, dict) and set(h.keys()).issubset(
                                                                    set(f.keys())) :
                                                                o = 0
                                                                for d in h.keys() :
                                                                    if str(h[d]) == str(f[d]) :
                                                                        o += 1
                                                                if str(o) == str(len(h.keys())) :
                                                                    s += 1

                                                    # 列表下级不是字典的情况
                                                    else :
                                                        for y in req[i][n] :
                                                            if not isinstance(y, dict) and str(h) in str(y) :
                                                                s += 1

                                                if str(s) != str(len(response[i][n])) :
                                                    return False
                                                # else :
                                                #     return False
                                        else :
                                            try :
                                                data_response = json.loads(response[i][n])
                                                data_req = json.loads(req[i][n])
                                                if isinstance(data_response, list) :
                                                    ab = 0
                                                    for ac in data_response :
                                                        if isinstance(ac, dict) :
                                                            for ar in data_req :
                                                                if isinstance(ar, dict) and set(ac.keys()).issubset(
                                                                        set(ar.keys())) :
                                                                    aer = 0
                                                                    for ace in ac.keys() :
                                                                        if str(ac[ace]) == str(ar[ace]) :
                                                                            aer += 1
                                                                    if str(aer) == str(len(ac.keys())) :
                                                                        ab += 1
                                                    if str(ab) != str(len(data_response)) :
                                                        return False

                                                elif isinstance(data_response, dict) :
                                                    ae = 0
                                                    for aq in data_response.keys() :
                                                        if str(data_response[aq]) == str(json.loads(req[i][n])[aq]) :
                                                            ae += 1
                                                    if str(len(data_response)) != str(ae) :
                                                        return False
                                            except :
                                                if str(response[i][n]) not in str(req[i][n]) :
                                                    return False

                        # 判断返回值是列表，结果是否相等
                        elif isinstance(response[i], list) :
                            # print(response[i])
                            if not isinstance(req[i], list) :
                                return False
                            else :
                                w = 0
                                for l in response[i] :
                                    if isinstance(l, dict) :
                                        for r in req[i] :
                                            if isinstance(r, dict) and set(l.keys()).issubset(set(r.keys())) :
                                                e = 0
                                                for c in l.keys() :
                                                    if str(l[c]) in str(r[c]) :
                                                        e += 1
                                                if str(e) == str(len(l.keys())) :
                                                    w += 1
                                    else :
                                        for q in req[i] :
                                            if not isinstance(q, dict) and str(l) == str(q) :
                                                w += 1
                                if str(w) != str(len(response[i])) :
                                    return False

                        # 其他类型，转字符串，直接判断是否相等
                        else :
                            if str(response[i]) not in str(req[i]) :
                                return False
                return True

            else:
                if "string_data" in response.keys():
                    if response["string_data"] == req :
                        return True
                    else:
                        return False
                else:
                    return False

        elif isinstance(req, list) and isinstance(response, list) :
            # print(response[i])
            if not isinstance(req, list) :
                return False
            else :
                w = 0
                for l in response :
                    if isinstance(l, dict) :
                        for r in req :
                            if isinstance(r, dict) and set(l.keys()).issubset(set(r.keys())) :
                                e = 0
                                for c in l.keys() :
                                    if str(l[c]) in str(r[c]) :
                                        e += 1
                                if str(e) == str(len(l.keys())) :
                                    w += 1
                    else :
                        for q in req :
                            if not isinstance(q, dict) and str(l) == str(q) :
                                w += 1
                if str(w) != str(len(response)) :
                    return False
            return True

        else :
            print("数据不是json结构")
            return False

    # post请求
    @classmethod
    def do_post(cls, url, data=None, headers=None) :
        """
        post请求，执行方法
        :param url:
        :param data:
        :param headers:
        :return:
        """
        if headers != "" and headers is not None :
            # res = requests.post(url=url, json=data, headers=headers)
            if data != "" and data is not None :
                # print(url, json.dumps(data), json.dumps(headers))
                if isinstance(headers, dict) :
                    # print(url, data, headers)
                    res = requests.post(url=url, json=data, headers=headers)
                elif isinstance(headers, str) :
                    headers = json.loads(headers)
                    res = requests.post(url=url, json=data, headers=headers)
                else :
                    headers = str(headers)
                    headers = json.loads(headers)
                    res = requests.post(url=url, json=data, headers=headers)
            else :
                # print(url, data, headers)
                res = requests.post(url=url, headers=headers)
        else :
            # res = requests.post(url=url, json=data)
            if data != "" and data is not None :
                res = requests.post(url=url, json=data)
            else :
                res = requests.post(url=url)
        # return res.json()
        return res.text
        # get请求

    @classmethod
    def do_get(cls, url, data=None, headers=None) :
        """
        get请求，执行方法
        :param url:
        :param data:
        :param headers:
        :return:
        """
        if headers != "" and headers is not None :
            if data != "" and data is not None :
                a = ''
                if isinstance(data, str) :
                    data = json.loads(data)
                for i in data.keys() :
                    a = a + "&" + str(i) + "=" + str(data[i])
                url = url + a

                if isinstance(headers, str) :
                    headers = json.loads(headers)

                res = requests.get(url=url, headers=headers)
            else :
                res = requests.get(url=url, headers=headers)

        else :
            if data != "" and data is not None :
                a = '&'
                for i in data.keys() :
                    a = a + "&" + str(i) + "=" + str(data[i])
                url = url + a
                res = requests.post(url=url)
            else :
                res = requests.post(url=url)
            # res = requests.get(url=url, data=data)
        return res.text
        # 调用post、get请求

    def run_method(self, method, url, data=None, headers=None) :
        try :
            if method.upper() == "POST" :
                res = self.do_post(url=url, data=data, headers=headers)
            else :
                res = self.do_get(url=url, data=data, headers=headers)
            return res
        except Exception as error :
            return {"error" : error}

    @classmethod
    def run_method_text(cls, method, url, **kwargs) :
        session = requests.session()
        req = session.request(method, url, **kwargs)
        print(req)
        return req.text

    @classmethod
    def login_token(cls, url, data, headers=None) :
        """
        #登录接口处理
        :param url:
        :param data:
        :param headers:
        :return:
        """
        if headers is not None :
            res = requests.post(url=url, json=data, headers=headers)
            token = res.json()['data']['token']
            json1 = res.json()

        else :
            res = requests.post(url=url, json=data)
            token = res.json()['data']['token']
            json1 = res.json()
        return token, json1

    @classmethod
    def update_token(cls) :
        # from http.client import HTTPConnection
        # HTTPConnection.debuglevel = 1

        def update_token_inside() :
            """
            内部调用接口，万能token
            :return:
            """
            url1 = "https://testauth.lian-ou.com/auth/login/token"
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
            url1 = url1 + St.SignatureEncryption().get_sign(payload)['Splicing'] + "&key=g90dAOmkjOljWtOr"
            response = requests.request("POST", url1, headers=headers, json=payload)
            tokenInside = response.json()['data']['token']
            return tokenInside

        # 获取内部token方法
        token_inside = update_token_inside()
        data_list = Bl.ExecuteBusiness().get_token_headers()
        token_list = {"inside" : str(token_inside)}
        for l in data_list :
            app_name = l[0]  # 项目名
            # token_list_upper = [ele.upper() for ele in token_list if isinstance(ele, str)]
            # 机构端的登录接口请求头比较特殊
            header = l[1]  # 请求头
            auth_type = l[2]  # 认证方式
            request_type = l[3]  # 请求方式
            url = l[4]  # 请求url
            body = l[5]  # 请求体
            if str(l[2]) == "3" :
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

                token_1 = RequestProcessing().run_method(method=request_type, url=url, data=body, headers=header)
                # 正则获取符合的数据
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
                continue
        Ro.ExecuteRedis().Write_App_token(json.dumps(token_list))
        return "更新成功"

    @classmethod
    def getAPhoneNumber(cls) :
        second = random.choice([3, 4, 5, 7, 8])
        third = {
            3 : random.randint(0, 9),
            4 : random.choice([5, 7, 9]),
            5 : random.choice([i for i in range(10) if i != 4]),
            7 : random.choice([i for i in range(9) if i != 4]),
            8 : random.randint(0, 9),
        }[second]
        last = "".join(str(random.randint(0, 9)) for i in range(8))
        return "1{}{}{}".format(second, third, last)

    @classmethod
    def GBK2312(cls) :
        req5 = ''
        for i in range(5) :
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x} {body:x}'
            val = bytes.fromhex(val).decode('gb2312')
            req5 = req5 + val
        return req5

    @classmethod
    def GenerateCases(cls, parameter, token, parameter_one=None, response_one=None, parameterType_one=None) :
        global count
        # from http.client import HTTPConnection
        # HTTPConnection.debuglevel = 1
        """
        数据处理，合成数据，调用执行用例
        :return:
        """
        # 获取数据据redis需要修改的缓存数据
        all_req_data = json.loads(Ro.ExecuteRedis().Read_App_data()["data"])
        ac = parameter
        header_list = Bl.ExecuteBusiness().get_token_headers()
        header_dict = {}
        for i in header_list :
            header_dict[i[0]] = i[1]
        app_name = ac[1]  # 项目名
        request_type = ac[6]  # 请求类型
        response = ac[8]  # 预计输出结果给
        case_seq = ac[12]  # 测试用例
        case_title = ac[13]  # 测试标题
        relate = json.loads(ac[11])  # 关联用例
        header_data = json.loads(header_dict[app_name])  # 请求头
        parameter_data = ac[7]
        parameterType = ac[14]  # 参数类型
        parameter_data_file = ''    # 文件入参
        # 单接口运行逻辑
        if parameter_one is not None and response_one is not None and parameterType_one is not None :
            parameter_data = parameter_one
            response = response_one
            parameterType = parameterType_one

        if parameter_data is not None and "这里是一个随机数" in str(parameter_data) :
            abc = '7' + str(random.randint(10000000000000, 99999999999999))
            parameter_data = parameter_data.replace('这里是一个随机数', abc)  # 入参，并处理随机数

        if parameter_data is not None and "这里是一个随机电话号码" in str(parameter_data) :
            number = RequestProcessing.getAPhoneNumber()
            parameter_data = parameter_data.replace('这里是一个随机电话号码', number)  # 入参，并处理随机数

        if parameter_data is not None and "这是一个随机汉字" in str(parameter_data) :
            chinese = RequestProcessing.GBK2312()
            parameter_data = parameter_data.replace('这是一个随机汉字', chinese)  # 入参，并处理随机数

        if parameter_data is not None and "这是一个随机时间" in str(parameter_data) :
            timeStamp = int(time.time())
            random_time = random.randint(1640793600, timeStamp)
            timeArray = time.localtime(random_time)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            parameter_data = parameter_data.replace('这是一个随机时间', otherStyleTime)  # 入参，并处理随机数

        # 修好获取的请求的参数
        if str(case_seq) in all_req_data.keys() :
            parameter_data = DataProcessing().ModifyData(json.loads(parameter_data), all_req_data[str(case_seq)])
        else :
            parameter_data = json.loads(parameter_data)
        token_data = token[app_name]
        url = ac[2] + "://" + ac[4] + ac[5]  # 请求接口
        if parameter_data == '' :
            parameter_data = ''

        # 上传文件接口特殊处理
        elif str(parameterType) == str(3) :
            new_parameter_data = {}
            url = url + (St.SignatureEncryption().get_sign(new_parameter_data))["Splicing"]

        else :
            if str(parameterType) == "1" and isinstance(parameter_data, dict):
                for l in parameter_data.keys() :
                    if not isinstance(parameter_data[l], (str, int)) :
                        # parameter[l] = json.dumps(parameter[l])
                        # print(parameter_data[l])
                        str_1 = json.dumps(parameter_data[l])
                        str_1.replace('\\', '\\\\')
                        str_1.replace('"', '\"')
                        parameter_data[l] = str_1
                url = url + (St.SignatureEncryption().get_sign(parameter_data))["Splicing"]

        # 内部接口调用
        if str(ac[10]) == "2" :
            header_data["authorization"] = "Bearer " + token["inside"]

        elif str(ac[10]) == "3" :
            header_data["authorization"] = "Bearer " + token_data

        elif str(ac[10]) == "1" :

            # 机构端token特殊处理
            if app_name.upper() == "DOCGROUP" :
                Special_list = ["OVERVIEW", "SILKBAG", "SHOPGOODS"]
                if len(re.findall(r'.com/(.+?)/', url)) != 0 and re.findall(r'.com/(.+?)/', url)[
                    0].upper() in Special_list :
                    header_data["from-web-location"] = "YD"
                    header_data["authorization"] = "Bearer " + token["DocGroup"]
                else :
                    header_data["authorization"] = "Bearer " + token["DocGroup"]


            elif app_name.upper() == "LOSCRM" :
                if len(re.findall(r'.com/(.+?)/', url)) != 0 and re.findall(r'.com/(.+?)/', url)[
                    0].upper() == "CLIENT" :

                    header_data["from-web-location"] = "SCRM"
                    header_data["authorization"] = "Bearer " + token["LoScrm"]

                else :
                    header_data["from-web-location"] = "SCRM"
                    header_data["authorization"] = "Bearer " + token["DocGroup_scrm"]

            elif app_name.upper() == "LOCWDZ" :
                header_data["x-logw-modular"] = "du-cwdz"
                # header_data["Sec-Fetch-Mode"] = "cors"
                header_data["authorization"] = "Bearer " + token["locwdz"]
                # print(header_data)

            elif app_name.upper() == "DOCSTUDIO" :
                # tokem不带Bearer 的项目
                list_doc = ["SHOPPINGMALL", "AUTHORIZE", "DOCGROUP", "APIREQUESTLOGGET", "GIFT", "INQUIRY",
                            "PRESCRIPTION", "PRESCRIPTIONORDER", "ROLEAUTHORITH", "ROLE", "SHIPADDRESSINFO",
                            "WEBSTUDIO", "WX", "FASTINQUIRY", "USER"]
                # 内部token列表
                list_doc2 = ["CMS", "DOCGROUP", "ADMIN"]
                list_doc3 = []
                if len(re.findall(r'.com/(.+?)/', url)) != 0 and re.findall(r'.com/(.+?)/', url)[
                    0].upper() in list_doc :
                    header_data["authorization"] = token_data

                # 内部token的控制器
                elif len(re.findall(r'.com/(.+?)/', url)) != 0 and re.findall(r'.com/(.+?)/', url)[
                    0].upper() in list_doc2 :
                    # header_data["x-logw-modular"] = "docgroup"
                    header_data["authorization"] = "Bearer " + token["inside"]

                else :
                    header_data["authorization"] = "Bearer " + token_data
                    # header_data["authorization"] = token_data

            # 药店端请求
            elif app_name.upper() == "APPSERVICE" :
                header_data["access_token"] = token_data
                # print(header_data)

            # # 商家中心的token，请求头的处理
            # elif app_name.upper() == "CommodityCenter":
            #     header_data["access_token"] = token_data
            #     header_data["x-logw-modular"] = "commoditycenter"
            #     # print(header_data)

            else :
                header_data["authorization"] = "Bearer " + token_data

        else :
            header_data["authorization"] = "Bearer " + token_data
            print(header_data)
            # print("不存在的认证方式")

        def req_method(request_type_2, url_2, parameter_data_2, header_data_2, parameter_data_file_2=None) :
            try :
                if str(parameterType) == "1" :
                    reqs_2 = RequestProcessing().run_method(method=request_type_2, url=url_2, data=parameter_data_2,
                                                            headers=header_data_2)
                elif str(parameterType) == "3" :
                    reqs_2 = RequestProcessing().run_method_text(method=request_type_2, url=url_2,
                                                                 data=parameter_data_2,
                                                                 files=parameter_data_file_2,
                                                                 headers=header_data_2)
                elif str(parameterType) == "2":
                    if  "string_body" in json.loads(parameter_data_2).keys() :
                        parameter_data_2 = json.loads(parameter_data_2)["string_body"]

                    reqs_2 = RequestProcessing().run_method_text(method=request_type_2, url=url_2,
                                                                 data=parameter_data_2,
                                                                 headers=header_data_2)

                else :
                    reqs_2 = RequestProcessing().run_method_text(method=request_type_2, url=url_2,
                                                                 data=parameter_data_2,
                                                                 headers=header_data_2)
            except Exception as error :
                reqs_2 = json.dumps({"error" : str(error)})
            return reqs_2

        # 判断请求头类型
        # Json格式请求
        if parameterType == 1 :
            header_data["Content-Type"] = "application/json"

        # Test格式请求
        elif parameterType == 2 :
            header_data["Content-Type"] = "text/plain"
            header_data["Accept"] = "*/*"
            print(parameter_data)
            parameter_data = json.dumps(parameter_data)
            print(parameter_data)

        # 文件格式请求
        elif parameterType == 3 :
            del header_data["Content-Type"]
            parameter_data_list = []
            if isinstance(parameter_data, dict):
                if "file" in parameter_data.keys():
                    parameter_data_file = parameter_data["file"]
                    if isinstance(parameter_data_file, list) :
                        for i in parameter_data_file :
                            data_key = list(i.keys())[0]
                            data_value = i[data_key]
                            path_name = pathlib.PurePath(data_value)
                            file_name, file_extension = os.path.splitext(data_value)
                            if file_extension == ".xls":
                                file_type = "application/vnd.ms-excel"
                            elif file_extension == ".xlsx":
                                file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            elif file_extension ==  ".jpg" :
                                file_type = "image/jpeg"
                            else:
                                file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            file_1 = (data_key, (path_name.name, open(data_value, 'rb'),
                                                 file_type))
                            parameter_data_list.append(file_1)
                        parameter_data_file = parameter_data_list

                if "data" in parameter_data.keys():
                    parameter_data_data = parameter_data["data"]
                    parameter_data = parameter_data_data

            else :
                print("入参格式错误")

        # 打印必要参数
        print("")
        print("用例编号：" + str(case_seq))
        print("用例标题：" + str(case_title))
        print("项目名：" + app_name)
        # print("请求数据：" + json.dumps(parameter_data, ensure_ascii=False))
        print("请求数据：" + str(parameter_data))
        print("用例断言值：" + response)
        print("接口名：" + url)
        print("请求头：" + json.dumps(header_data, ensure_ascii=False))

        if str(ac[10]) == "9" and app_name == 'hosptial' :
            count_loop = 0
            reqs = req_method(request_type, url, parameter_data, header_data, parameter_data_file)
            while 'code' in str(reqs) and str(json.loads(reqs)['code']) != '1' and count_loop < 10 :
                reqs = req_method(request_type, url, parameter_data, header_data, parameter_data_file)
                count_loop += 1
                print(count_loop)
                time.sleep(2)

        # 目前有这些项目返回数据是这样['fzdoc', 'workorder']
        elif str(ac[10]) == "9" :
            count_loop = 0
            time.sleep(3)
            reqs = req_method(request_type, url, parameter_data, header_data, parameter_data_file)
            while 'code' in str(reqs) and str(json.loads(reqs)['code']) == '1' and json.loads(reqs)[
                'data'] == [] and count_loop < 10 :
                reqs = req_method(request_type, url, parameter_data, header_data, parameter_data_file)
                count_loop += 1
                print(count_loop)
                time.sleep(2)

        else :
            reqs = req_method(request_type, url, parameter_data, header_data,parameter_data_file)

        print("实际返回值：" + reqs)

        if "contact" in relate.keys() and relate['contact'] is not None and relate[
            'contact'] != "" and "关联用例id" not in str(relate) :
            try :
                reqs = json.loads(reqs)
            except :
                print("数据有问题，不进行缓存数据更新")
            DataProcessing().req_data(reqs, relate)
            reqs = json.dumps(reqs, ensure_ascii=False)

        return case_seq, response, reqs, url

    @classmethod
    def runCaseOne(cls, parameter, parameter_one, response_one, parameterType_one) :
        token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
        if str(parameter[1]) not in token.keys() :
            RequestProcessing().update_token()
            time.sleep(2)
            token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
        case_seq, response, reqs, url = RequestProcessing().GenerateCases(parameter, token, parameter_one, response_one,
                                                                          parameterType_one)
        count_3 = 0
        if "oken过期" in str(reqs) and count_3 < 1 :
            print("token过期")
            # 更新token
            RequestProcessing().update_token()
            # 获取token
            token1 = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])
            case_seq, response, reqs, url = RequestProcessing().GenerateCases(parameter, token1, parameter_one,
                                                                              response_one, parameterType_one)
            count_3 += 1

        try :
            result = RequestProcessing().AssertResults(response=response, req=reqs)
        except :
            result = False
        return reqs, result, url


# if __name__ == '__main__':
#     print('???')
