from Base.BaseElementEnmu import Element as be
from Base.BaseOperate import OperateElement
from Base.BaseYaml import getYam
from PageObject.SumResult import statistics_result


class CardsSortPage:

    def __init__(self, kwargs):
        self.driver = kwargs["driver"]
        if kwargs.get("launch_app", "0") == "0":
            self.driver.launch_app()
        self.path = kwargs["path"]
        self.operateElement = OperateElement(self.driver)
        self.isOperate = True
        test_msg = getYam(self.path)
        self.testInfo = test_msg["testinfo"]
        self.testCase = test_msg["testcase"]
        self.testcheck = test_msg["check"]
        self.device = kwargs["device"]
        self.logTest = kwargs["logTest"]
        self.caseName = kwargs["caseName"]
        self.get_value = []
        self.location = []
        self.msg = ""

    def operate(self):
        for item in self.testCase:
            m_s_g = self.msg + "\n" if self.msg != "" else ""

            result = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
            if not result["result"]:
                msg = "Falló durante la ejecución, verifique si el elemento existe" + item["element_info"]
                print(msg)
                self.msg = m_s_g + msg
                self.testInfo[0]["msg"] = msg
                self.isOperate = False
                return False

            if item.get("operate_type", "0") == "location":
                app = {}
                web_element = self.driver.find_elements_by_id(item["element_info"])[item["index"]]
                start = web_element.location

                app["startX"] = start["x"]
                app["startY"] = start["y"]

                size1 = web_element.size

                width = size1["width"]
                height = size1["height"]

                endX = width + app["startX"]
                endY = height + app["startY"]

                app["endX"] = endX - 20
                app["endY"] = endY - 60

                self.location.append(app)

            if item.get("operate_type", "0") == be.GET_VALUE:
                self.get_value.append(result["text"])

            if item.get("is_swpie", "0") != "0":
                print(self.location)
                self.driver.swipe(self.location[0]["endX"], self.location[0]["endY"], self.location[1]["endX"],
                                  self.location[1]["endY"] + 10)

        return True

    def checkPoint(self, kwargs={}):
        result = self.check()
        if result is not True and be.RE_CONNECT:
            self.msg = "El caso de uso falló y se volvió a conectar una vez, el motivo del fallo:" + self.testInfo[0][
                "msg"]
            self.logTest.buildStartLine(self.caseName + "_No se pudo volver a conectar")
            self.operateElement.switchToNative()
            self.driver.launch_app()
            self.isOperate = True
            self.operate()
            self.get_value = []
            self.location = ""
            result = self.check()
            self.testInfo[0]["msg"] = self.msg
        statistics_result(result=result, testInfo=self.testInfo, caseName=self.caseName,
                          driver=self.driver, logTest=self.logTest, devices=self.device,
                          testCase=self.testCase,
                          testCheck=self.testcheck)
        return result

    def check(self):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""

        if self.isOperate:
            for item in self.testcheck:
                resp = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
                if not resp["result"]:
                    msg = "Por favor marque el elemento" + item["element_info"] + "existe"
                    self.msg = m_s_g + msg
                    print(msg)
                    self.testInfo[0]["msg"] = msg
                    result = False
                if resp['text'] not in self.get_value:
                    msg = "Falló la clasificación de tarjetas" + str(
                        self.get_value) + "Los primeros datos de la tarjeta en la página de inicio actual son:" + resp[
                              "text"] + "El primer valor de la tarjeta que se clasifica correctamente es: " + ".".join(
                        self.get_value)
                    self.msg = m_s_g + msg
                    print(msg)
                    self.testInfo[0]["msg"] = msg
                    break
        else:
            result = False
        return result


if __name__ == "__main__":
    pass
