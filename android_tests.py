import time
import unittest

from appium import webdriver


class AndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '10'
        desired_caps['deviceName'] = 'Mi A2'
        desired_caps['appPackage'] = 'com.android.calculator2'
        desired_caps['appActivity'] = '.Calculator'
        remote = "http://127.0.0.1:" + "4723" + "/wd/hub"
        self.d = webdriver.Remote(remote, desired_caps)

    def tearDown(self):
        self.d.quit()

    def test_plus(self):
        self.d.find_element_by_id("com.google.android.calculator:id/digit_1").click()
        self.d.find_element_by_id("com.google.android.calculator:id/digit_9").click()
        time.sleep(1)
        result = self.d.find_element_by_id("com.google.android.calculator:id/result_preview")
        if result is not None:
            print("Prueba aprobada")
        else:
            print("Prueba fallida")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
