import random
import sys

sys.path.append("..")
from Base.BaseIosCommand import *
from Base.BaseRunner import ParametrizedTestCase
from TestCase.HomeTest import HomeTest
from Base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool
import unittest
from Base.BaseInit import init
from Base.BaseStatistics import countDate, writeExcel
from datetime import datetime

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        print("----runnerPool------")
        print(getDevices[i])
        _initApp = {}
        devices = getDevices[i]["devices"]
        _initApp["deviceName"] = get_ios_product_name(devices)
        _initApp["platformVersion"] = get_ios_version(devices)
        _initApp["platformName"] = "ios"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["bundleId"] = "com.huawei.works"
        _initApp["udid"] = devices
        _initApp["automationName"] = "XCUITest"
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    starttime = datetime.now()
    suite = unittest.TestSuite()

    suite.addTest(ParametrizedTestCase.parametrize(HomeTest, param=devices))

    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.now()
    countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "segundo")


if __name__ == '__main__':

    devicess = get_ios_devices()
    if len(devicess) > 0:
        l_devices = []
        init()

        for dev in devicess:
            app = {}
            app["devices"] = dev
            app["port"] = str(random.randint(4700, 4900))
            app["bport"] = str(random.randint(4700, 4900))
            l_devices.append(app)

        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
        writeExcel()
        appium_server.stop_server(l_devices)
    else:
        print("No hay dispositivo Android disponible")
