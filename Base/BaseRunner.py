import os
import unittest

from appium import webdriver

from Base.BaseLog import myLog

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def appium_testcase(devices):
    desired_caps = {}

    if str(devices["platformName"]).lower() == "android":

        desired_caps['udid'] = devices["deviceName"]
        desired_caps['app'] = devices["app"]


    else:

        desired_caps['bundleId'] = devices["bundleId"]
        desired_caps['udid'] = devices["udid"]

    desired_caps['platformVersion'] = devices["platformVersion"]
    desired_caps['platformName'] = devices["platformName"]
    desired_caps["automationName"] = devices['automationName']
    desired_caps['deviceName'] = devices["deviceName"]
    desired_caps["noReset"] = "True"
    desired_caps['noSign'] = "True"
    desired_caps["unicodeKeyboard"] = "True"
    desired_caps["resetKeyboard"] = "True"
    desired_caps["systemPort"] = devices["systemPort"]

    remote = "http://127.0.0.1:" + str(devices["port"]) + "/wd/hub"

    driver = webdriver.Remote(remote, desired_caps)
    return driver


class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should  
        inherit from this class.  
    """

    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        global devicess
        devicess = param

    @classmethod
    def setUpClass(cls):
        pass
        cls.driver = appium_testcase(devicess)
        cls.devicesName = devicess["deviceName"]
        cls.logTest = myLog().getLog(cls.devicesName)

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        cls.driver.quit()
        pass

    def tearDown(self):
        pass

    @staticmethod
    def parametrize(testcase_klass, param=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite
