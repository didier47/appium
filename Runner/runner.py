import random
import sys
import time

from TestCase.eribank_test import EribankTest

sys.path.append("..")
import platform
from Base.BaseAndroidPhone import *
from Base.BaseAdb import *
from Base.BaseRunner import ParametrizedTestCase
from TestCase.HomeTest import HomeTest
from Base.BaseAppiumServer import AppiumServer
from multiprocessing import Pool
import unittest
from Base.BaseInit import init, mk_file
from Base.BaseStatistics import countDate, writeExcel
from datetime import datetime
from Base.BaseApk import ApkInfo

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def kill_adb():
    if platform.system() == "Windows":

        os.system(PATH("../app/kill5037.bat"))
    else:
        os.popen("killall adb")
    os.system("adb start-server")


def runnerPool(getDevices):
    devices_Pool = []

    for i in range(0, len(getDevices)):
        _pool = []
        _initApp = {}
        _initApp["deviceName"] = getDevices[i]["devices"]
        _initApp["platformVersion"] = getPhoneInfo(devices=_initApp["deviceName"])["release"]
        _initApp["platformName"] = "android"
        _initApp["port"] = getDevices[i]["port"]
        _initApp["automationName"] = "uiautomator2"
        _initApp["systemPort"] = getDevices[i]["systemPort"]
        _initApp["app"] = getDevices[i]["app"]
        _initApp[
            "appPackage"] = 'com.experitest.ExperiBank'  # Nota (Si conozco de antemano el nombre del paquete y el activity main, no es necesario utilizar el código para descompilar la app
        _initApp["appActivity"] = 'com.experitest.ExperiBank.LoginActivity'
        _pool.append(_initApp)
        devices_Pool.append(_initApp)

    pool = Pool(len(devices_Pool))
    pool.map(runnerCaseApp, devices_Pool)
    pool.close()
    pool.join()


def runnerCaseApp(devices):
    starttime = datetime.now()
    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(EribankTest, param=devices))  # nota Test a realizar
    suite.addTest(ParametrizedTestCase.parametrize(EribankTest, param=devices))

    unittest.TextTestRunner(verbosity=2).run(suite)
    endtime = datetime.now()
    countDate(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str((endtime - starttime).seconds) + "segundo")


if __name__ == '__main__':

    kill_adb()

    devicess = AndroidDebugBridge().attached_devices()
    if len(devicess) > 0:
        mk_file()
        l_devices = []
        for dev in devicess:
            app = {}
            app["devices"] = dev
            init(dev)
            app["port"] = str(random.randint(4700, 4900))
            app["bport"] = str(random.randint(4700, 4900))
            app["systemPort"] = str(random.randint(4700, 4900))
            app["app"] = PATH("../app/eribank.apk")  # nota App a utilizar (Opcional)

            l_devices.append(app)

        appium_server = AppiumServer(l_devices)
        appium_server.start_server()
        runnerPool(l_devices)
        writeExcel()
        appium_server.stop_server(l_devices)
    else:
        print("No hay dispositivo Android disponible")
