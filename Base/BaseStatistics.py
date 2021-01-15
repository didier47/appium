import os

import xlsxwriter

from Base.BaseElementEnmu import Element
from Base.BaseExcel import OperateReport
from Base.BasePickle import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def countInfo(**kwargs):
    _info = {}
    step = ""
    check_step = ""

    for case in kwargs["testCase"]:
        step = step + case["info"] + "\n"

    if type(kwargs["testCheck"]) == list:
        for check in kwargs["testCheck"]:
            check_step = check_step + check["info"] + "\n"
    elif type(kwargs["testCheck"]) == dict:
        check_step = kwargs["testCheck"]["info"]
    else:
        print("Obtener error de datos de paso del punto de control, verifique")
        print(kwargs["testCheck"])

    _info["step"] = step
    _info["checkStep"] = check_step

    if kwargs["result"]:
        _info["result"] = "por"
        kwargs["logTest"].checkPointOK(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                       checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                           "msg", " "))
    else:
        _info["result"] = "fracaso"
        _info["img"] = kwargs["logTest"].checkPointNG(driver=kwargs["driver"], caseName=kwargs["testInfo"][0]["title"],
                                                      checkPoint=kwargs["caseName"] + "_" + kwargs["testInfo"][0].get(
                                                          "msg", " "))
    _info["id"] = kwargs["testInfo"][0]["id"]
    _info["title"] = kwargs["testInfo"][0]["title"]
    _info["caseName"] = kwargs["caseName"]
    _info["phoneName"] = kwargs["phoneName"]
    _info["msg"] = kwargs["testInfo"][0].get("msg", "")
    _info["info"] = kwargs["testInfo"][0]["info"]

    writeInfo(data=_info, path=PATH("../Log/" + Element.INFO_FILE))


def countSumNoDevices(devices, result, _read, phone_name):
    if _read is None:
        _read = []

    app = {"phone_name": phone_name, "pass": 0, "fail": 0, "device": devices}
    if result:
        app["pass"] = 1
    else:
        app["fail"] = 1
    _read.append(app)
    write(data=_read, path=PATH("../Log/" + Element.DEVICES_FILE))
    print(read(PATH("../Log/" + Element.DEVICES_FILE)))

    return


def countSumDevices(devices, result, phone_name):
    _read = readInfo(PATH("../Log/" + Element.DEVICES_FILE))
    if _read:
        for item in _read:
            if item["device"] == devices:
                if result:
                    item["pass"] = item["pass"] + 1
                else:
                    item["fail"] = item["fail"] + 1
                write(data=_read, path=PATH("../Log/" + Element.DEVICES_FILE))
                return
    countSumNoDevices(devices, result, _read, phone_name=phone_name)
    print(read(PATH("../Log/" + Element.DEVICES_FILE)))


def countSum(result):
    data = {"sum": 0, "pass": 0, "fail": 0}
    _read = read(PATH("../Log/sum.pickle"))
    if _read:
        data = _read
    data["sum"] = data["sum"] + 1
    if result:
        data["pass"] = data["pass"] + 1
    else:
        data["fail"] = data["fail"] + 1
    write(data=data, path=PATH("../Log/" + Element.SUM_FILE))


def countDate(testDate, testSumDate):
    print("--------- countDate------")
    data = read(PATH("../Log/" + Element.SUM_FILE))
    print(data)
    if data:
        data["testDate"] = testDate
        data["testSumDate"] = testSumDate
        write(data=data, path=PATH("../Log/" + Element.SUM_FILE))
    else:
        print("Las estadísticas fallaron")


def writeExcel():
    workbook = xlsxwriter.Workbook(PATH('../Report/' + Element.REPORT_FILE))
    worksheet = workbook.add_worksheet("Resumen de la prueba")
    worksheet2 = workbook.add_worksheet("Detalles de la prueba")
    operateReport = OperateReport(workbook)
    operateReport.init(worksheet, read(PATH("../Log/" + Element.SUM_FILE)),
                       read(PATH("../Log/" + Element.DEVICES_FILE)))
    operateReport.detail(worksheet2, readInfo(PATH("../Log/" + Element.INFO_FILE)))
    operateReport.close()


if __name__ == '__main__':
    writeExcel()
