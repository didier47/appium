from Base.BaseElementEnmu import Element as be
from Base.BaseOperate import OperateElement
from Base.BaseYaml import getYam
from PageObject.SumResult import statistics_result


class CollectSwipeDelPage:

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
        self.msg = ""

    def operate(self):
        m_s_g = self.msg + "\n" if self.msg != "" else ""
        for item in self.testCase:
            result = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)
            if not result["result"]:
                msg = "Falló durante la ejecución, verifique si el elemento existe" + item["element_info"]
                print(msg)
                self.testInfo[0]["msg"] = msg
                self.msg = m_s_g + msg
                self.isOperate = False
                return False

            if item.get("operate_type", "0") == be.SWIPE_LEFT:
                web_element = self.driver.find_elements_by_id(item["element_info"])[item["index"]]
                start = web_element.location

                startx = start["x"]
                starty = start["y"]

                size1 = web_element.size

                width = size1["width"]
                height = size1["height"]

                endX = width + startx
                endY = height + starty
                self.driver.swipe(endX - 50, endY, starty + 500, endY)
            if item.get("operate_type", "0") == be.GET_VALUE:
                self.get_value.append(result["text"])
        return True

    def checkPoint(self):
        result = self.check()
        if result is not True and be.RE_CONNECT:
            self.msg = "El caso de uso falló y se volvió a conectar una vez, el motivo del fallo:" + self.testInfo[0][
                "msg"]
            self.logTest.buildStartLine(self.caseName + "_No se pudo volver a conectar")

            self.driver.launch_app()
            self.isOperate = True
            self.get_value = []
            self.operate()
            result = self.check()
            self.testInfo[0]["msg"] = self.msg
        self.operateElement.switchToNative()

        statistics_result(result=result, testInfo=self.testInfo, caseName=self.caseName,
                          driver=self.driver, logTest=self.logTest, devices=self.device,
                          testCase=self.testCase,
                          testCheck=self.testcheck)
        return result

    def check(self, kwargs={}):
        result = True
        m_s_g = self.msg + "\n" if self.msg != "" else ""

        if self.isOperate:
            for item in self.testcheck:
                resp = self.operateElement.operate(item, self.testInfo, self.logTest, self.device)

                if not resp["result"]:
                    print("Operación fallida, más simple significa éxito")
                    result = True
                    break

                if resp["text"] in self.get_value:
                    msg = "Error en la eliminación de datos, los datos antes de la eliminación son: " + ".".join(
                        self.get_value) + "Los datos adquiridos actualmente son：" + resp["text"]
                    self.msg = m_s_g + msg
                    print(msg)
                    self.testInfo[0]["msg"] = msg
                    break
        else:
            result = False
        return result


if __name__ == "__main__":
    pass
