import os
import subprocess


class AndroidDebugBridge(object):
    def call_adb(self, command):
        command_result = ''
        command_text = 'adb %s' % command

        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    def fastboot(self, device_id):
        pass

    def attached_devices(self):

        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE).stdout.readlines()

        for item in result:
            t = item.decode().split("\tdevice")
            if len(t) >= 2:
                devices.append(t[0])

        return devices

    def get_state(self):
        result = self.call_adb("get-state")
        result = result.strip(' \t\n\r')
        return result or None

    def reboot(self, option):
        command = "reboot"
        if len(option) > 7 and option in ("bootloader", "recovery",):
            command = "%s %s" % (command, option.strip())
        self.call_adb(command)

    def push(self, local, remote):
        result = self.call_adb("push %s %s" % (local, remote))
        return result

    def pull(self, remote, local):
        result = self.call_adb("pull %s %s" % (remote, local))
        return result

    def sync(self, directory, **kwargs):
        command = "sync %s" % directory
        if 'list' in kwargs:
            command += " -l"
            result = self.call_adb(command)
            return result

    def open_app(self, packagename, activity):
        result = self.call_adb("shell am start -n %s/%s" % (packagename, activity))
        check = result.partition('\n')[2].replace('\n', '').split('\t ')
        if check[0].find("Error") >= 1:
            return False
        else:
            return True

    def get_app_pid(self, pkg_name):
        string = self.call_adb("shell ps | grep " + pkg_name)

        if string == '':
            return "the process doesn't exist."
        result = string.split(" ")

        return result[4]


if __name__ == '__main__':
    print(os.popen("adb devices", 'r').readline())
