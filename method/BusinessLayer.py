# -*- coding: utf-8 -*-
import time

import connect_mysql.ConnectDatabase as Db_connect
import CommonMethod.Message as Msg
import json
import method.RedisOperation as Rd


class ExecuteBusiness :
    """
    执行sql业务操作
    """

    def __init__(self) :
        self.cursor, self.db = Db_connect.ConnectMysql().MysqlReadingWrite()

    def __del__(self) :
        """
        关闭数据库连接池
        :return:
        """
        # print("销毁对象=================================")
        self.db.close()

    def ScreeningConditions(self) :
        """
        获取修改项目的项目名，是否需要修改
        :return:
        """
        sql = "SELECT DISTINCT(app_name) FROM api_case where IsRead = '1' ;"
        self.cursor.execute(sql)
        data_api = self.cursor.fetchall()
        data_list = []
        for i in data_api :
            data_list.append(i[0])
        return {"code" : "1", "msg" : "操作成功", "data" : {"list" : data_list}}

    def queryCaseInfo(self, isChange, app_name, apiPath, apiCase, apiRelate, pageIndex, pageSize) :
        """
        获取修改项目的项目名，是否需要修改
        :return:
        """
        # pageIndex = 5
        # pageSize = 20
        sql_count = "SELECT COUNT(*) FROM api_case WHERE Ischange = '{0}' AND IsRead = '1' AND app_name = '{1}' AND api_path LIKE '%{2}%' AND info_Relate LIKE '%{3}%' ".format(
            isChange, app_name, apiPath, str(apiRelate))
        sql = "SELECT case_seq,case_title,app_name,api_name,api_path,parameter,response, info_Relate,remarks FROM api_case WHERE Ischange = '{0}' AND IsRead = '1' AND app_name = '{1}' AND api_path LIKE '%{2}%' AND info_Relate LIKE '%{3}%' ".format(
            isChange, app_name, apiPath, str(apiRelate))
        if apiCase != "" and apiCase is not None :
            sql_count = "SELECT COUNT(*) FROM api_case WHERE" + " case_seq = '" + apiCase + "'"
            sql = "SELECT case_seq,case_title,app_name,api_name,api_path,parameter,response, info_Relate,remarks FROM api_case WHERE" + " case_seq = '" + apiCase + "'"
            # sql = sql + " and case_seq = '"+ apiCase +"'"
            # sql_count = sql_count + " and case_seq = '"+ apiCase +"'"

        elif apiRelate != "" and apiRelate is not None :
            sql_count = "SELECT COUNT(*) FROM api_case WHERE info_Relate LIKE '%{0}%' ".format(apiRelate)
            sql = "SELECT case_seq,case_title,app_name,api_name,api_path,parameter,response, info_Relate,remarks FROM api_case WHERE info_Relate LIKE '%{0}%' ".format(
                apiRelate)
        if pageIndex is None and pageSize is None :
            sql = sql + " limit 0,20"
        else :
            pageIndex = (int(pageIndex) - 1) * int(pageSize)
            sql = sql + " limit {0},{1}".format(pageIndex, pageSize)
        # print(sql)

        self.cursor.execute(sql)
        data_api = self.cursor.fetchall()

        self.cursor.execute(sql_count)
        total_count = self.cursor.fetchall()

        data_list = []
        # print(sql)
        for i in data_api :
            data_list.append(i)
        return {"code" : "1", "msg" : "操作成功", "total" : total_count[0][0], "data" : {"list" : data_list}}

    def DeleteCase(self, postData) :
        """
        删除不要的用例，isRead改成0
        :return:
        """
        # sql = "SELECT * FROM api_case WHERE case_seq = '{0}';".format(postData)
        sql = "UPDATE api_case SET IsRead = '0' WHERE case_seq = '{0}';".format(postData)
        self.cursor.execute(sql)
        self.db.commit()
        return {"code" : "1", "msg" : "操作成功"}

    def queryCaseAllInfo(self, postData) :
        """
        获取修改项目的项目名，是否需要修改
        :return:
        """
        sql = "SELECT * FROM api_case WHERE case_seq = '{0}';".format(postData)
        self.cursor.execute(sql)
        data_api = self.cursor.fetchall()
        data_list = data_api[0]
        data = {
            "caseId" : data_list[0],
            "appName" : data_list[2],
            "apiType" : data_list[3],
            "apiHost" : data_list[6],
            "apiPath" : data_list[7],
            "parameter" : data_list[8],
            "response" : data_list[9],
            "relate" : data_list[14],
            "remarks" : data_list[15],
            "caseTitle" : data_list[16],
            "parameter_type" : data_list[17]
        }
        return {"code" : "1", "msg" : "操作成功", "data" : data}

    def submitDelete(self, postData) :
        """
        提交删除数据的接口
        :return:
        """
        sql = "UPDATE  api_case SET IsRead = '0' WHERE case_seq = '{}'".format(postData)
        self.cursor.execute(sql)
        self.db.commit()  # 不能省，必须要加commit来提交到mysql中去确认执行
        return {"code" : "1", "msg" : "删除成功"}

    def submitUpdateData(self, case_seq, parameter, response, relate, caseTitle, parameter_type) :
        """
        提交更新数据的接口
        :return:
        """
        # parameter = parameter.replace('\"', '\\"')
        sql = "UPDATE api_case SET parameter = %s,response = %s, Ischange = '0', info_Relate= %s, case_title= %s, parameter_type = %s WHERE case_seq = %s"
        self.cursor.execute(sql, (parameter, response, relate, caseTitle, parameter_type, case_seq))
        self.db.commit()
        return {"code" : "1", "msg" : "修改成功"}

    def submitInsertData(self, case_seq, parameter, response, relate, caseTitle, parameter_type) :
        """
        提交插入数据的接口
        :return:
        """
        # sql = "insert into api_case SELECT  NULL case_seq,api_id, app_name,api_type,request_type,api_name,api_host,api_path,%s parameter,%s response,'0' Ischange,'1' IsRead,auth_type, actual_value, %s info_Relate FROM api_case WHERE case_seq = %s"
        sql = "insert into api_case(case_seq,api_id, app_name,api_type,request_type,api_name,api_host,api_path,parameter, response, Ischange, IsRead,auth_type, actual_value, info_Relate, remarks, case_title, parameter_type) SELECT  NULL case_seq,api_id, app_name,api_type,request_type,api_name,api_host,api_path,%s parameter,%s response,'0' Ischange,'1' IsRead,auth_type, actual_value, %s info_Relate, remarks, %s case_title, %s parameter_type FROM api_case WHERE case_seq = %s"
        self.cursor.execute(sql, (parameter, response, relate, caseTitle, parameter_type, case_seq))
        self.db.commit()
        return {"code" : "1", "msg" : "插入成功"}

    def Home(self) :
        """
        首页
        :return:
        """
        sql = "SELECT case_seq,app_name,api_type,request_type,api_name,api_host,api_path,parameter,response,auth_type FROM api_case WHERE Ischange = '1' AND IsRead = '1'"
        self.cursor.execute(sql)
        data_api = self.cursor.fetchall()
        return data_api

    def getCaseInfo(self, postData) :
        """
        通过用例id放回用例详情
        :return:
        """
        sql = "SELECT case_seq,parameter,expect_value FROM api_case WHERE case_seq = '{}'".format(postData)
        self.cursor.execute(sql)
        data_api = self.cursor.fetchall()
        return {"caseId" : data_api[0], "parameter" : data_api[0], "expectValue" : data_api[0]}

    def update_case_table(self) :
        """
        更新用例表，获取最新的接口用例数据
        :return:
        """
        """
        修改用例表的IsRead，Ischange字段，改成IsRead=0，Ischange=0，条件：用例表的api_id不存在接口表中
        """

        def modify(data_url, data_cases) :
            """
            判断是否需要修改
            :return:是否修改
            """
            # 接收接口表的数据，返回一个字典{"api_id":"data"}
            url_list = list(data_url)
            url_dict = dict(url_list)
            # 接收用例表的数据，返回一个字典{"api_id":"data"}
            cases_list = list(data_cases)
            # print(cases_list)
            # cases_dict = dict(cases_list)
            # 新建一个接收需要修改的列表
            tup_change = []
            # 新建一个接收不需要修改的列表
            tup_Nochange = []
            for i in cases_list :
                cases_path = i[0]  # 路径
                api_body = i[1]  # 请求体
                cases_id = i[2]  # 用例id
                # 获取接口表单个接口body的内容，dict
                # print(cases_id)
                if url_dict[cases_path] == "" :
                    url_dict_i_dict = ""
                else :
                    try:
                        url_dict_i_dict = json.loads(url_dict[cases_path])
                    except :
                        url_dict_i_dict = ""

                # 获取用例表单个接口body的内容，dict
                if api_body == "" :
                    case_dict_i_dict = ""
                else :
                    try :
                        case_dict_i_dict = json.loads(api_body)
                    except :
                        case_dict_i_dict = ""

                # 新建一个需要修改的元组
                if isinstance((case_dict_i_dict, url_dict_i_dict),dict) and set(dict(case_dict_i_dict).keys()).issubset(set(dict(url_dict_i_dict).keys())) :
                    tup_Nochange.append(cases_id)

                # 不是对象类型，不作修改
                elif isinstance((case_dict_i_dict, url_dict_i_dict),int):
                    tup_Nochange.append(cases_id)

                else :
                    tup_change.append(cases_id)
            tup_change_tup1 = tuple(tup_change)
            tup_Nochange_tup1 = tuple(tup_Nochange)
            # print(tup_change_tup1)
            # print(tup_Nochange_tup1)
            return tup_change_tup1, tup_Nochange_tup1

        # 去掉不要的接口
        # sql_url_del = "UPDATE api_info A RIGHT JOIN api_case B ON B.api_id=A.api_id SET B.IsRead='0', B.Ischange='1' WHERE A.api_path IS NULL"
        sql_url_del = "UPDATE  api_info A RIGHT JOIN api_case B ON B.api_id=A.api_id SET B.IsRead=0 WHERE A.api_path IS NULL"
        self.cursor.execute(sql_url_del)
        self.db.commit()  # 不能省，必须要加commit来提交到mysql中去确认执行

        """
        修改用例表的IsRead，Ischange字段，改成IsRead=1，Ischange=1，条件：用例表的api_id存在table表中
        并且判断存在的用例是否需要修改body
        """
        # 修改接口表有，用例表有，但状态IsRead=0，的接口
        sql_url_add = "UPDATE api_info a inner join api_case b on B.api_id=A.api_id SET b.IsRead = '1' WHERE b.IsRead = '0';"
        self.cursor.execute(sql_url_add)
        self.db.commit()  # 不能省，必须要加commit来提交到mysql中去确认执行

        """
        修改用例表的IsRead，Ischange字段，改成IsRead=1，Ischange=1，条件：接口表中有的api_id，用例表中没有对应api_id
        """
        Relate = {"level":"关联用例等级","type":"1","contact":{"关联用例id":{"inq（关联用例的参数）":"inq（接口返回的参数）","docName（关联用例的参数）":"docName（接口返回的参数）"}}}
        Relate = json.dumps(Relate, ensure_ascii=False)
        sql_url_change = "insert into api_case(case_seq, api_id, app_name,api_type,request_type,api_name,api_host,api_path,parameter,response,Ischange,IsRead,auth_type, actual_value, info_Relate, remarks, parameter_type) SELECT case_seq, A.api_id, A.app_name,A.api_type,A.request_type,A.api_name,A.api_host,A.api_path,A.parameter,A.response,'1' Ischange,'1' IsRead,A.auth_type, '' actual_value, %s info_Relate, A.remarks, 1 parameter_type FROM  api_info A LEFT JOIN api_case B ON A.api_id = B.api_id WHERE B.api_id IS NULL;"
        self.cursor.execute(sql_url_change, Relate)
        self.db.commit()  # 不能省，必须要加commit来提交到mysql中去确认执行
        # 关闭数据库连接

        try :

            # 查询接口表需要执行的接口
            sql_url = "select api_id,parameter from api_info;"
            self.cursor.execute(sql_url)
            data_api = self.cursor.fetchall()
            # 查询用例表需
            # sql_casc = "SELECT api_id,parameter,case_seq FROM api_case WHERE IsRead='1';"
            sql_casc = "SELECT api_id,parameter,case_seq FROM api_case WHERE IsRead='1' AND Ischange = '0';"
            self.cursor.execute(sql_casc)
            data_case = self.cursor.fetchall()
            tup_change_tup, tup_Nochange_tup = modify(data_url=data_api, data_cases=data_case)
            # print( tup_Nochange_tup)
            # print(tup_change_tup)
            # 更新是否需要修改的数据

            if len(tup_change_tup) == 0 :
                print("不需要修改")
            elif len(tup_change_tup) == 1 :
                tup_change_tup_update = "UPDATE api_case SET Ischange='1' WHERE case_seq = '{0}'".format(
                    tup_change_tup[0])
                self.cursor.execute(tup_change_tup_update)
            elif len(tup_change_tup) > 1 :
                tup_change_tup_update = "UPDATE api_case SET Ischange='1' WHERE case_seq in {0}".format(tup_change_tup)
                self.cursor.execute(tup_change_tup_update)
            return {"code" : "1", "msg" : "更新成功"}

        except :
            # 通知企业微信机器人。更新项目，更新用例出现错误
            Msg.MessageNotification().msg_qw_case()
            return {"code" : "1", "msg" : "更新成功，用例状态更新失败"}

    def getCaseExecute(self, caseId = None, appName = None) :
        """
        获取需要执行的用例
        :return:
        """
        if caseId is not None :
            api_list = [1, 1]
            sql = "select CONCAT(REPLACE(json_extract(info_Relate,'$.level'),'{}',''), case_seq) acn, app_name, api_type, api_name, api_host, api_path, request_type, parameter, response, actual_value, auth_type, info_Relate, case_seq,case_title, parameter_type FROM api_case WHERE case_seq =%s ".format('"')
            self.cursor.execute(sql, caseId)
            results = self.cursor.fetchall()
            # print(list(results))
            return list(results), list(api_list)

        elif appName is not None :
            sql_api_count = "SELECT COUNT(api_id) FROM api_info where app_name = %s ;"
            sql_api_execute = "SELECT COUNT(DISTINCT api_id) FROM api_case WHERE Ischange = '0' AND IsRead = '1' AND app_name = %s ;"
            # sql = "select CONCAT(REPLACE(json_extract(info_Relate,'$.level'),'{}',''), case_seq) acn, app_name, api_type, api_name, api_host, api_path, request_type, parameter, response, actual_value, auth_type, info_Relate, case_seq FROM api_case WHERE Ischange = '0' AND IsRead = '1' and app_name = %s".format('"')
            # 获取单项目的单接口用例
            sql = "select CONCAT(REPLACE(json_extract(info_Relate,'$.level'),'{0}',''), case_seq) acn, app_name, api_type, api_name, api_host, api_path, request_type, parameter, response, actual_value, auth_type, info_Relate, case_seq,case_title, parameter_type FROM api_case WHERE Ischange = '0' AND IsRead = '1' and app_name = %s and  REPLACE(json_extract(info_Relate,'$.type'),'{1}','') = '1'".format('"','"')
            api_list = []
            try :
                # 执行sql语句
                self.cursor.execute(sql_api_count, appName)
                api_count = self.cursor.fetchall()
                api_list.append(api_count[0][0])

                self.cursor.execute(sql_api_execute, appName)
                api_execute = self.cursor.fetchall()
                api_list.append(api_execute[0][0])

                # 获取所有的记录
                self.cursor.execute(sql, appName)
                results = self.cursor.fetchall()
                # print(list(results))

                # 获取关联接口用例
                case_list = ExecuteBusiness().get_case_data(appName)
                case_tuple = tuple(case_list)
                if case_tuple :
                    sql_1 = "select CONCAT(REPLACE(json_extract(info_Relate,'$.level'),'{0}',''), case_seq) acn, app_name, api_type, api_name, api_host, api_path, request_type, parameter, response, actual_value, auth_type, info_Relate, case_seq,case_title, parameter_type FROM api_case WHERE case_seq in {1} ".format('"', case_tuple)
                    self.cursor.execute(sql_1)
                    api_execute_1 = self.cursor.fetchall()
                else:
                    api_execute_1 = case_tuple
                results_all = list(results) + list(api_execute_1)
                # print(api_execute_1)
                return results_all, list(api_list)
            except :
                print("getData Error!")

        else:
            sql_api_count = "SELECT COUNT(api_id) FROM api_info;"
            sql_api_execute = "SELECT COUNT(DISTINCT api_id) FROM api_case WHERE Ischange = '0' AND IsRead = '1';"
            sql = "select CONCAT(REPLACE(json_extract(info_Relate,'$.level'),'{}',''), case_seq) acn, app_name, api_type, api_name, api_host, api_path, request_type, parameter, response, actual_value, auth_type, info_Relate, case_seq,case_title, parameter_type FROM api_case WHERE Ischange = '0' AND IsRead = '1'".format('"')  # and app_name in ('hosptial','fzdoctor' ) and case_seq in ('7407')
            api_list = []
            try :
                # 执行sql语句
                self.cursor.execute(sql_api_count)
                api_count = self.cursor.fetchall()
                api_list.append(api_count[0][0])

                self.cursor.execute(sql_api_execute)
                api_execute = self.cursor.fetchall()
                api_list.append(api_execute[0][0])

                # 获取所有的记录
                self.cursor.execute(sql)
                results = self.cursor.fetchall()
                return list(results), list(api_list)
            except :
                print("getData Error!")

    def update(self, case_id, result1) :
        query = "UPDATE api_case SET actual_value = '{0}' WHERE case_seq= '{1}'".format(result1, case_id)
        sql1 = "SELECT actual_value FROM api_case WHERE case_seq = '{}'".format(case_id)
        self.cursor.execute(query)
        self.db.commit()
        self.cursor.execute(sql1)
        # 获取所有的记录
        results = self.cursor.fetchall()
        # 打印表数据
        for row in results :
            # print(row)
            api_name = row[0]
            # print(eval(result1), api_name)
            if api_name == result1 :
                print("用例表数据库更新成功")
            else :
                print("update Error!")

    def get_token_headers(self) :
        """
        获取项目信息
        :return:
        """
        sql = "select app_name, headers, auth_type, request_type, url, body from pro_info;"
        self.cursor.execute(sql)
        ab = self.cursor.fetchall()
        return ab


    def upward_query_case(self, caseId_list, all_list) :
        """
        向上找
        :return:
        """
        if caseId_list:
            for caseId in caseId_list:
                sql = "SELECT case_seq FROM `api_case`  WHERE info_Relate like '%{0}%'".format(caseId)
                self.cursor.execute(sql)
                ab = self.cursor.fetchall()
                # print(ab)
                if ab :
                    # 判断查出来的数据是否是主流程用例
                    qwe = []
                    for l in ab :
                        dict_l = str(l[0])
                        # 判断
                        sql = "SELECT REPLACE(json_extract(info_Relate,'$.type'),'{0}','') FROM `api_case`  WHERE case_seq = %s".format('"')
                        self.cursor.execute(sql, dict_l)
                        abc = self.cursor.fetchall()
                        if abc :
                            if str(abc[0][0]) == '2' :
                                qwe.append(dict_l)
                            else :
                                continue
                        else :
                            continue
                    all_list = qwe + all_list
                    all_list = ExecuteBusiness().upward_query_case(qwe, all_list)
                else:
                    continue
            return all_list
        else:
            return all_list

    def downward_query_case(self, caseId_list, all_list) :
        """
        向下找
        :return:
        """
        if caseId_list:
            for caseId in caseId_list:
                sql = "SELECT info_Relate FROM `api_case`  WHERE REPLACE(json_extract(info_Relate,'$.type'),'{0}','') = '2' and case_seq = %s".format('"')
                self.cursor.execute(sql, caseId)
                ab = self.cursor.fetchall()
                if ab :
                    # 循环获取每个用例
                    for l in ab :
                        dict_l = json.loads(l[0])
                        if 'contact' in dict_l.keys():
                            dict_list1 = dict_l['contact']
                            dict_list = [*dict_list1]

                            # 判断查出来的数据是否是主流程用例
                            for K in dict_list :
                                sql = "SELECT REPLACE(json_extract(info_Relate,'$.type'),'{0}','') FROM `api_case`  WHERE case_seq = %s".format('"')
                                self.cursor.execute(sql, K)
                                ab = self.cursor.fetchall()
                                if ab:
                                    if str(ab[0][0]) == '2':
                                        continue
                                    else:
                                        dict_list.remove(K)
                                else:
                                    dict_list.remove(K)

                            # 移除默认的用例数据，关联用例id
                            if '关联用例id' in dict_list:
                                dict_list.remove('关联用例id')
                            all_list = all_list + dict_list
                            all_list = ExecuteBusiness().downward_query_case(dict_list, all_list)
                else:
                    continue

            return all_list
        else:
            return all_list

    def get_case_data(self, appName) :
        """
        获取项目信息
        :return:
        """
        sql = "SELECT case_seq FROM `api_case`  WHERE REPLACE(json_extract(info_Relate,'$.type'),'{}','') = '2' and app_name = %s ;".format(
            '"')
        self.cursor.execute(sql, appName)
        ab = self.cursor.fetchall()

        # 处理查询到的用例数据
        case_list = []
        for i in ab :
            case = i[0]
            case_list.append(str(case))
        case_1 = ExecuteBusiness().upward_query_case(case_list, case_list)
        case_2 = ExecuteBusiness().downward_query_case(case_list, case_list)

        case_list = case_1 + case_2
        case_list = list(set(case_list))
        return case_list

    def queryProEnum(self):
        """
        查询所有pro 枚举值
        :return:
        """
        sql = "select distinct(app_name) from pro_info ;"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        pro_ls = []
        auth_dict = {'外部认证':'1','内部认证':'2','商家后台':'3'}
        for i in data:
            pro_ls.append(i[0])
        data = {'proName':pro_ls,'authType':auth_dict}
        return {"code":"1","msg":"操作成功","data":data}

    def queryProInfo(self,proName):
        """
        查询完整项目信息
        :return:
        """
        sql = "select * from pro_info where app_name like %s;"
        self.cursor.execute(sql,proName)
        data = self.cursor.fetchall()
        proInfo = {'proName':data[0][0],'proDeclare':data[0][6],'reqHeader':data[0][1],'reqUrl':data[0][2],'reqType':data[0][3],'authType':data[0][4],'secretKey':data[0][5],'reqBody':data[0][7]}
        return {'code':'1','msg':'操作成功','data':proInfo}

    def addOrEditProInfo(self,state):
        """
        新增/编辑项目信息
        :return:
        """
        if state != None:
            if state == '0':
                sql = 'insert into pro_info (app_name,headers,url,request_type,auth_type,`sercert_key/iv`,name,body) values(%s,%s,%s,%s,%s,%s,%s,%s); '
                self.cursor.execute(sql, ('test', '', '', '', '', '', '', ''))
            elif state == '1':
                pass
                sql = 'update pro_info set headers=%s,url=%s,request_type=%s,auth_type=%s,`sercert_key/iv`=%s, name = %s,body=%s where app_name = %s;'
                self.cursor.execute(sql, ('','','','','','测试', '测试测试body', 'test'))
        self.db.commit()


if __name__ == '__main__':
    execute = ExecuteBusiness()
    execute.addOrEditProInfo('1')
