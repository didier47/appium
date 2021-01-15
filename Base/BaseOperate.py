import os
import re
import time

import appium.common.exceptions
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from Base.BaseElementEnmu import Element as be


class OperateElement:
    def __init__(self, driver=""):
        self.driver = driver

    def findElement(self, mOperate):
        try:
            if type(mOperate) == list:
                for item in mOperate:
                    if item.get("is_webview", "0") == 1:
                        self.switchToWebview()
                    elif item.get("is_webview", "0") == 2:
                        self.switchToNative()

                    t = item["check_time"] if item.get("check_time", "0") != "0" else be.WAIT_TIME
                    WebDriverWait(self.driver, t).until(lambda x: self.elements_by(item))
                return {"result": True}
            if type(mOperate) == dict:
                if mOperate.get("is_webview", "0") == 1 and self.switchToWebview() is False:
                    print("No se pudo cambiar a la vista web, confirme si está en la página de vista web")
                    return {"result": False, "webview": False}
                elif mOperate.get("is_webview", "0") == 2:
                    self.switchToNative()
                if mOperate.get("element_info", "0") == "0":
                    return {"result": True}
                t = mOperate["check_time"] if mOperate.get("check_time",
                                                           "0") != "0" else be.WAIT_TIME
                WebDriverWait(self.driver, t).until(lambda x: self.elements_by(mOperate))
                return {"result": True}
        except selenium.common.exceptions.TimeoutException:

            return {"result": False, "type": be.TIME_OUT}
        except selenium.common.exceptions.NoSuchElementException:

            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.WebDriverException:

            return {"result": False, "type": be.WEB_DROVER_EXCEPTION}

    def operate(self, mOperate, testInfo, logTest, device):
        res = self.findElement(mOperate)
        if res["result"]:
            return self.operate_by(mOperate, testInfo, logTest, device)
        else:
            return res

    def operate_by(self, operate, testInfo, logTest, device):
        try:
            info = operate.get("element_info", " ") + "_" + operate.get("operate_type", " ") + str(operate.get(
                "code", " ")) + operate.get("msg", " ")
            logTest.buildStartLine(testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + info)
            print("==Pasos de operación: %s==" % info)

            if operate.get("operate_type", "0") == "0":
                return {"result": True}

            elements = {
                be.SWIPE_DOWN: lambda: self.swipeToDown(),
                be.SWIPE_UP: lambda: self.swipeToUp(),
                be.CLICK: lambda: self.click(operate),
                be.GET_VALUE: lambda: self.get_value(operate),
                be.SET_VALUE: lambda: self.set_value(operate),
                be.ADB_TAP: lambda: self.adb_tap(operate, device),
                be.TAP: lambda: self.tap(operate),
                be.GET_CONTENT_DESC: lambda: self.get_content_desc(operate),
                be.PRESS_KEY_CODE: lambda: self.press_keycode(operate)

            }
            return elements[operate.get("operate_type")]()
        except IndexError:
            logTest.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + operate["element_info"] + "Error de índice")

            return {"result": False, "type": be.INDEX_ERROR}

        except selenium.common.exceptions.NoSuchElementException:
            logTest.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + operate[
                    "element_info"] + "El elemento de la página no existe o no está cargado")

            return {"result": False, "type": be.NO_SUCH}
        except selenium.common.exceptions.StaleElementReferenceException:
            logTest.buildStartLine(
                testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + operate[
                    "element_info"] + "Los elementos de la página han cambiado")

            return {"result": False, "type": be.STALE_ELEMENT_REFERENCE_EXCEPTION}
        except KeyError:

            return {"result": True}

    def adb_tap(self, mOperate, device):

        bounds = self.elements_by(mOperate).location
        x = str(bounds["x"])
        y = str(bounds["y"])

        cmd = "adb -s " + device + " shell input tap " + x + " " + y
        print(cmd)
        os.system(cmd)

        return {"result": True}

    def tap(self, operate):
        x1 = operate["bounds"][0][0]
        y1 = operate["bounds"][0][1]

        x2 = operate["bounds"][0][1]
        y2 = operate["bounds"][1][1]
        self.driver.tap([(x1, y1), (x2, y2)], operate.get("duration", 300))

        return {"result": True}

    def toast(self, xpath, logTest, testInfo):
        logTest.buildStartLine(
            testInfo[0]["id"] + "_" + testInfo[0]["title"] + "_" + "Buscar elementos emergentes_" + xpath)
        try:
            WebDriverWait(self.driver, 10, 0.5).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            return {"result": True}
        except selenium.common.exceptions.TimeoutException:
            return {"result": False}
        except selenium.common.exceptions.NoSuchElementException:
            return {"result": False}

    def click(self, mOperate):

        if mOperate["find_type"] == be.find_element_by_id or mOperate["find_type"] == be.find_element_by_xpath:
            self.elements_by(mOperate).click()
        elif mOperate.get("find_type") == be.find_elements_by_id:
            self.elements_by(mOperate)[mOperate["index"]].click()
        return {"result": True}

    def press_keycode(self, mOperate):
        self.driver.press_keycode(mOperate.get("code", 0))
        return {"result": True}

    def get_content_desc(self, mOperate):
        result = self.elements_by(mOperate).get_attribute("contentDescription")
        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    def switchToNative(self):
        self.driver.switch_to.context("NATIVE_APP")

    def switchToWebview(self):
        try:
            n = 1
            while n < 10:
                time.sleep(3)
                n = n + 1
                print(self.driver.contexts)
                for cons in self.driver.contexts:
                    if cons.lower().startswith("webview"):
                        self.driver.switch_to.context(cons)

                        self.driver.execute_script('document.querySelectorAll("html")[0].style.display="block"')
                        self.driver.execute_script('document.querySelectorAll("head")[0].style.display="block"')
                        self.driver.execute_script('document.querySelectorAll("title")[0].style.display="block"')
                        print("切换webview成功")
                        return {"result": True}
            return {"result": False}
        except appium.common.exceptions.NoSuchContextException:
            print("No se pudo cambiar la vista web")
            return {"result": False, "text": "appium.common.exceptions.NoSuchContextException异常"}

    def swipeLeft(self, mOperate):
        width = self.driver.get_window_size()["width"]
        height = self.driver.get_window_size()["height"]
        x1 = int(width * 0.75)
        y1 = int(height * 0.5)
        x2 = int(width * 0.05)
        self.driver(x1, y1, x2, y1, 600)

    def swipeToDown(self):
        height = self.driver.get_window_size()["height"]
        x1 = int(self.driver.get_window_size()["width"] * 0.5)
        y1 = int(height * 0.25)
        y2 = int(height * 0.75)

        self.driver.swipe(x1, y1, x1, y2, 1000)

        print("--swipeToDown--")
        return {"result": True}

    def swipeToUp(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        self.driver.swipe(width / 2, height * 3 / 4, width / 2, height / 4)
        print("Realizar dominadas")
        return {"result": True}

    def swipeToRight(self):
        height = self.driver.get_window_size()["height"]
        width = self.driver.get_window_size()["width"]
        x1 = int(width * 0.05)
        y1 = int(height * 0.5)
        x2 = int(width * 0.75)
        self.driver.swipe(x1, y1, x1, x2, 1000)

        print("--swipeToUp--")

    def set_value(self, mOperate):
        self.elements_by(mOperate).send_keys(mOperate["msg"])
        return {"result": True}

    def get_value(self, mOperate):

        if mOperate.get("find_type") == be.find_elements_by_id:
            element_info = self.elements_by(mOperate)[mOperate["index"]]
            if mOperate.get("is_webview", "0") == 1:
                result = element_info.text
            else:
                result = element_info.get_attribute("text")
            re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
            return {"result": True, "text": "".join(re_reulst)}

        element_info = self.elements_by(mOperate)
        if mOperate.get("is_webview", "0") == 1:
            result = element_info.text
        else:
            result = element_info.get_attribute("text")

        re_reulst = re.findall(r'[a-zA-Z\d+\u4e00-\u9fa5]', result)
        return {"result": True, "text": "".join(re_reulst)}

    def click_windows(self, device):
        try:
            button0 = 'com.huawei.systemmanager:id/btn_allow'

            button_list = [button0]
            for elem in button_list:
                find = self.driver.find_element_by_id(elem)
                WebDriverWait(self.driver, 1).until(lambda x: self.elements_by(find(elem)))
                bounds = find.location
                x = str(bounds["x"])
                y = str(bounds["y"])
                cmd = "adb -s " + device + " shell input tap " + x + " " + y
                print(cmd)
                os.system(cmd)
                print("==点击授权弹框_%s==" % elem)
        except selenium.common.exceptions.TimeoutException:

            pass
        except selenium.common.exceptions.NoSuchElementException:

            pass
        except selenium.common.exceptions.WebDriverException:

            pass

    def elements_by(self, mOperate):

        elements = {
            be.find_element_by_id: lambda: self.driver.find_element_by_id(mOperate["element_info"]),
            be.find_element_by_xpath: lambda: self.driver.find_element_by_xpath(mOperate["element_info"]),
            be.find_element_by_css_selector: lambda: self.driver.find_element_by_css_selector(mOperate['element_info']),
            be.find_element_by_class_name: lambda: self.driver.find_element_by_class_name(mOperate['element_info']),
            be.find_elements_by_id: lambda: self.driver.find_elements_by_id(mOperate['element_info'])

        }
        return elements[mOperate["find_type"]]()
