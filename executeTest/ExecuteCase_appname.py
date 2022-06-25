import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import method.CaseOperation as Hc
from CommonMethod.ddt import ddt, data
import CommonMethod.HTMLTestRunner as HTMLTestRunner
import time
import unittest
import method.BusinessLayer as Bl
import method.CaseOperation as Co
import method.RedisOperation as Ro
import method.RedisOperation as Rd
import json

# 获取用例执行数据
req2 = Ro.ExecuteRedis().Read_App_name()
app_name = req2['data']
# app_name = 'hosptial'
case_list, api_list= Bl.ExecuteBusiness().getCaseExecute(appName=app_name)

@ddt
class Test(unittest.TestCase) :

    token = "token"
    app_name = "测试"
    # 更新token
    @classmethod
    def setUpClass(cls):
        """
        启动测试前，需要更新项目的token
        :return:
        """
        global token
        try:
            Co.RequestProcessing.update_token()
            data_init = {}
            Rd.ExecuteRedis().Write_App_data(json.dumps(data_init, ensure_ascii=False))
            token = json.loads(Rd.ExecuteRedis().Read_App_token()["data"])

            if app_name == "fzdoctor":
                # 去掉现有医生端，药师端接诊的问诊单
                Co.SubmitInq().NoPass(token)
                time.sleep(2)

                # 提交问诊
                for L in range(2) :
                    Co.SubmitInq().save_open('330401355994966')

            elif app_name == "hosptial":
                Co.SubmitInq().NoPass(token)
                time.sleep(2)

                # 提交问诊
                for L in range(2) :
                    Co.SubmitInq().save_open('330401355994966')
                # 提交美团工单
                Co.SubmitInq().save_workOrder()

            elif app_name == "workorder":
                # 提交美团工单
                Co.SubmitInq().save_workOrder()

        except Exception as e:
            print("初始化用例执行环境失败")
            return e

    # def setUp(self) :
    #     print("===Start!===")
    #
    # def tearDown(self) :
    #     print("===end!===")

    @data(*case_list)
    # @unpack  # @unpack，那么[3,2,1]被分解开，按照用例中的三个参数传递
    def test_minus(self, parameter) :
        case_seq, actual_value, req, url = Hc.RequestProcessing().GenerateCases(parameter, token)
        # print(actual_value)
        result = Co.RequestProcessing().AssertResults(response = actual_value, req= req)
        print(result)
        self.assertTrue(result, msg=None)


if __name__ == "__main__" :
    if case_list :
        s = unittest.TestSuite()
        s.addTests(unittest.TestLoader().loadTestsFromTestCase(Test))
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + '.html'
        test_file = os.path.join(rootPath, 'report', app_name)
        if not os.path.exists(test_file):
            os.mkdir(test_file)
        filePath = os.path.join(rootPath, 'report', app_name, now)
        fp = open(filePath, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口自动化测试报告', api_count=api_list, app_name=app_name)
        runner.run(s)
        fp.close()

    else:
        print("用例为空")
