# -*- coding: utf-8 -*-
import time
from flask import Flask, render_template, request
import method.BusinessLayer as Mb
import executeTest.ExecuteCase as Ec
import method.RedisOperation as Ro
import socket
import method.CaseOperation as Co
from os import path, mkdir, rename
import sys

curPath = path.abspath(path.dirname(__file__))
sys.path.append(curPath)


def get_host_ip():
    """
    获取服务器ip地址
    :return:
    """
    global s
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('10.0.0.1',8080))
        ip= s.getsockname()[0]
    finally:
        s.close()
    return ip

app = Flask(__name__)


@app.route('/update/caseTable', methods=['GET'])
def caseTable() :
    """
    更新用例表，获取最新的接口用例数据
    :return:
    """
    app_name = request.args.get("appName")
    Ro.ExecuteRedis().Write_App_name(app_name)
    req = Mb.ExecuteBusiness().update_case_table()
    return req


@app.route('/screeningConditions', methods=['GET'])
def Screening_conditions() :
    """
    获取修改项目的项目名，是否需要修改
    :return:
    """
    req = Mb.ExecuteBusiness().ScreeningConditions()
    return req


@app.route('/queryCaseInfo', methods=['POST'])
def queryCase_Info() :
    """
    获取修改项目的项目名，是否需要修改
    :return:
    """
    app_name = request.json.get("appName")
    isChange = request.json.get("isChange")
    apiPath = request.json.get("apiPath")
    apiCase = request.json.get("apiCase")
    apiRelate = request.json.get("apiRelate")
    pageIndex = request.json.get("pageIndex")
    pageSize = request.json.get("pageSize")

    if isChange == "是" :
        isChange = "1"
    elif isChange == "否" :
        isChange = "0"
    req = Mb.ExecuteBusiness().queryCaseInfo(isChange=isChange, app_name=app_name, apiPath=apiPath, apiCase=apiCase, apiRelate=apiRelate, pageIndex=pageIndex, pageSize=pageSize)
    return req


@app.route('/queryCaseAllInfo', methods=['POST'])
def queryCase_allInfo() :
    """
    获取修改项目的项目名，是否需要修改
    :return:
    """
    postData = request.json.get("caseId")
    req = Mb.ExecuteBusiness().queryCaseAllInfo(postData=postData)
    return req


@app.route('/submitDelete', methods=['POST'])
def submit_delete() :
    """
    提交删除数据的接口
    :return:
    """
    postData = request.json.get("caseId")
    req = Mb.ExecuteBusiness().DeleteCase(postData=postData)
    return req


@app.route('/submitUpdateData', methods=['POST'])
def submit_updateData() :
    """
    提交更新数据的接口
    :return:
    """
    case_seq = request.json.get("caseId")
    parameter = request.json.get("parameter")
    relate = request.json.get("relate")
    response = request.json.get("response")
    caseTitle = request.json.get("caseTitle")
    parameter_type = request.json.get("parameterType")
    req = Mb.ExecuteBusiness().submitUpdateData(case_seq=case_seq, parameter=parameter, response=response, relate=relate, caseTitle=caseTitle, parameter_type=parameter_type)
    return req


@app.route('/submitInsertData', methods=['POST'])
def submit_InsertData() :
    """
    提交插入数据的接口
    :return:
    """
    case_seq = request.json.get("caseId")
    parameter = request.json.get("parameter")
    response = request.json.get("response")
    relate = request.json.get("relate")
    caseTitle = request.json.get("caseTitle")
    parameter_type = request.json.get("parameterType")
    req = Mb.ExecuteBusiness().submitInsertData(case_seq=case_seq, parameter=parameter, response=response, relate=relate, caseTitle=caseTitle, parameter_type=parameter_type)
    return req


@app.route('/getCaseInfo', methods=['POST'])
def get_caseInfo() :
    """
    通过用例id放回用例详情
    :return:
    """
    postData = request.json.get("caseId")
    req = Mb.ExecuteBusiness().getCaseInfo(postData=postData)
    return req

@app.route('/runTest', methods=['POST'])
def runTest() :
    """
    通过用例id放回用例详情
    :return:
    """
    postData = request.json.get("caseId")
    parameterType = request.json.get("parameterType")
    parameter = request.json.get("parameter", None)
    response = request.json.get("response", None)
    results, api_list = Mb.ExecuteBusiness().getCaseExecute(caseId = postData)
    req, results, url = Co.RequestProcessing().runCaseOne(results[0], parameter, response, parameterType)
    return {"code": "1", "data": req, "results": results, "url": url}

@app.route('/test/FileUpload', methods=["POST", "GET"])
def FileUpload() :
    """
    测试环境文件上传功能
    :return:
    """
    if request.method == "GET" :
        return render_template("test.html")
    if request.method == "POST" :
        f = request.files["file"]
        new_time = time.time()

        file_all = path.join(curPath, "file")
        if not path.exists(file_all):
            mkdir(file_all)
        a = path.join(file_all, f.filename)
        b = path.join(file_all, str(int(new_time)) + f.filename)

        f.save(path.join(a))
        rename(a, b)
        return "上传成功，文件路径为：" + b

@app.route('/home', methods=['GET'])
def home() :
    """
    首页
    :return:
    """
    # req = Mb.ExecuteBusiness().Home()
    req = []
    return render_template('home.html', results=req, host=host_front)


@app.route('/submitUpdate', methods=['GET'])
def submit_update() :
    """
    提交更新数据的页面
    :return:
    """
    return render_template('submitUpdate.html', host=host_front)


@app.route('/submitInsert', methods=['GET'])
def submit_insert() :
    """
    提交插入数据的页面
    :return:
    """
    return render_template('submitInsert.html', host=host_front)


@app.route('/proInfo/queryProEnum',methods=['GET'])
def query_proName():
    """
    项目名称&认证方式
    :return:
    """
    result = Mb.ExecuteBusiness().queryProEnum()
    return result


@app.route('/proInfo/queryProInfo',methods=['POST'])
def query_proInfo():
    """
    项目信息
    :return:
    """
    proName = request.get_json()['proName']
    result = Mb.ExecuteBusiness().queryProInfo(proName)
    return result


@app.route('/proInfo/addOrEditProInfo',methods=['POST'])
def addoredit_proInfo():
    """
    新增或编辑项目信息
    :return:
    """
    proName = request.get_json()['proName']
    proDeclare = request.get_json()['proDeclare']
    reqHeader = request.get_json()['reqHeader']
    reqUrl = request.get_json()['reqUrl']
    authType = request.get_json()['authType']
    reqBody = request.get_json()['reqBody']
    info = {'proName':proName}




if __name__ == '__main__' :
    # app.debug = True  # 设置调试模式，生产模式的时候要关掉debug
    # 后端服务接口域名
    host = get_host_ip()
    # 172.25.0.151，开发环境ip

    if str(host) == '10.10.9.64' or str(host) == '10.10.9.4' or str(host) == '172.20.10.13':
        app.debug = True
        host_front = "{}:8058".format(host)
    else:
        app.debug = False
        host_front = "testautomated.lianouyiyuan.com"

    app.run(host=host, port="8058")