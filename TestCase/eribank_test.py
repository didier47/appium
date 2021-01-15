import os
import sys

from Base.BaseRunner import ParametrizedTestCase
from PageObject.Home.FirstOpenPage import FirstOpenPage

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class EribankTest(ParametrizedTestCase):
    def testFirstOpen(self):
        app = {"logTest": self.logTest, "driver": self.driver, "path": PATH("../yamls/home/eribank.yaml"),
               "device": self.devicesName, "caseName": sys._getframe().f_code.co_name}

        page = FirstOpenPage(app)
        page.operate()
        page.checkPoint()

    @classmethod
    def setUpClass(cls):
        super(EribankTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(EribankTest, cls).tearDownClass()
