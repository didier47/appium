from Base.BaseElementEnmu import Element
from Base.BaseFile import *
from Base.BasePickle import *

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def mk_file():
    destroy()
    mkdir_file(PATH("../Log/" + Element.INFO_FILE))
    mkdir_file(PATH("../Log/" + Element.SUM_FILE))
    mkdir_file(PATH("../Log/" + Element.DEVICES_FILE))

    data = read(PATH("../Log/" + Element.INFO_FILE))

    data["versionCode"] = "40"
    data["versionName"] = "1.4.0"
    data["packingTime"] = "2017/12/4 13:00"
    data["sum"] = 0
    data["pass"] = 0
    data["fail"] = 0
    write(data=data, path=PATH("../Log/" + Element.SUM_FILE))


def init(devices):
    pass


def destroy():
    remove_file(PATH("../Log/" + Element.INFO_FILE))
    remove_file(PATH("../Log/" + Element.SUM_FILE))
    remove_file(PATH("../Log/" + Element.DEVICES_FILE))


if __name__ == '__main__':
    print(destroy())
