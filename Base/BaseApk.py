import os
import re
import subprocess
from math import floor


class ApkInfo():
    def __init__(self, apkPath):
        self.apkPath = apkPath

    def getApkSize(self):
        size = floor(os.path.getsize(self.apkPath) / (1024 * 1000))
        return str(size) + "M"

    def getApkBaseInfo(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        if not match:
            raise Exception("can't get packageinfo")
        packagename = match.group(1)
        versionCode = match.group(2)
        versionName = match.group(3)

        print('packagename:' + packagename)
        print('versionCode:' + versionCode)
        print('versionName:' + versionName)
        return packagename, versionName, versionCode

    def getApkName(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        t = output.decode().split()
        for item in t:

            match = re.compile("application-label:(\S+)").search(item)
            if match is not None:
                return match.group(1)

    def getApkActivity(self):
        p = subprocess.Popen("aapt dump badging %s" % self.apkPath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        print("=====getApkActivity=========")
        match = re.compile("launchable-activity: name=(\S+)").search(output.decode())
        print("match=%s" % match)
        if match is not None:
            return match.group(1)


if __name__ == '__main__':
    pass
