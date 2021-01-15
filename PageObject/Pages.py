import os
import time

from Base.BaseElementEnmu import Element as be
from Base.BaseError import get_error
from Base.BaseOperate import OperateElement
from PageObject.SumResult import statistics_result

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class PagesObjects:

    def __init__(self, kwargs):
        self.driver = kwargs["driver"]
        if kwargs.get("launch_app", "0") == "0":
            self.driver.launch_app()

        self.operateElement = OperateElement(self.driver)
        self.isOperate = True
        self.test_msg = kwargs["test_msg"]
        self.testInfo = self.test_msg[1]["testinfo"]
        self.testCase = self.test_msg[1]["testcase"]
        self.testcheck = self.test_msg[1]["check"]
        self.device = kwargs["device"]
        self.logTest = kwargs["logTest"]
        self.caseName = kwargs["caseName"]
        self.get_value = []
        self.is_get = False
        self.msg = ""

    def operate(self):
        if self.test_msg[0] is False:
            self.isOperate = False
            return False
        for item in self.testCase:
            m_s_g = self.msg + "\n" if self.msg != "" else ""
            result = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
            if not result["result"]:
                msg = "Falló durante la ejecución, verifique si el elemento existe" + item[
                    "element_info"] + "," + result.get("text", " ")
                if not result.get("webview", True):
                    msg = "No se pudo cambiar a la vista web, confirme si está en la página de vista web"
                print(msg)
                self.msg = m_s_g + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False
            if item.get("is_time", "0") != "0":
                time.sleep(item["is_time"])
                print("--Espere---")

            if item.get("operate_type", "0") == be.GET_VALUE or item.get("operate_type", "0") == be.GET_CONTENT_DESC:
                self.get_value.append(result["text"])
                self.is_get = True

        return True

    def checkPoint(self, kwargs={}):
        result = self.check(kwargs)
        if self.test_msg[0] is not False:
            if result is not True and be.RE_CONNECT:
                self.msg = "El caso de uso falló y se volvió a conectar una vez, el motivo del fallo:" + \
                           self.testInfo[0]["msg"]
                self.logTest.buildStartLine(self.caseName + "_No se pudo volver a conectar")
                self.operateElement.switchToNative()
                self.driver.launch_app()
                self.isOperate = True
                self.get_value = []
                self.is_get = False
                self.operate()
                result = self.check(kwargs)
                self.testInfo[0]["msg"] = self.msg
            self.operateElement.switchToNative()

        statistics_result(result=result, testInfo=self.testInfo, caseName=self.caseName,
                          driver=self.driver, logTest=self.logTest, devices=self.device,
                          testCase=self.testCase,
                          testCheck=self.testcheck)

    def check(self, kwargs):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""

        if self.isOperate:
            for item in self.testcheck:
                if kwargs.get("check", be.DEFAULT_CHECK) == be.TOAST:
                    result = \
                        self.operateElement.toast(item["element_info"], testInfo=self.testInfo, logTest=self.logTest)[
                            "result"]
                    if result is False:
                        m = get_error(
                            {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["info"]})
                        self.msg = m_s_g + m
                        print(m)
                        self.testInfo[0]["msg"] = m
                    break
                else:
                    resp = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)

                if kwargs.get("check", be.DEFAULT_CHECK) == be.DEFAULT_CHECK and not resp["result"]:
                    m = get_error(
                        {"type": be.DEFAULT_CHECK, "element_info": item["element_info"], "info": item["info"]})
                    self.msg = m_s_g + m
                    print(m)
                    self.testInfo[0]["msg"] = m
                    result = False
                    break
        else:
            result = False
        return result
