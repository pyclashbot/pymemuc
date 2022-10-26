# a wrapper for memuc.exe as a library to control virual machines
# documentation detailed in memuc_documentation.md

from subprocess import Popen, PIPE
from os.path import join, normpath
from typing import Literal
from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx


class PyMemuc:
    def __init__(self) -> None:
        self.memuc_path = join(self.get_memu_top_level(), "memuc.exe")

    def get_memu_top_level(self) -> str:
        """locate the path of the memu directory

        Returns:
            str: the path of the memu directory
        """
        try:
            akey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MEmu"
            areg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            akey = OpenKey(areg, akey)
        except FileNotFoundError:
            akey = (
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MEmu"
            )
            areg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            akey = OpenKey(areg, akey)
        return str(join(normpath(QueryValueEx(akey, "InstallLocation")[0]), "Memu"))

    def run(self, args, non_blocking=False):
        args.insert(0, self.memuc_path)
        args += "-t" if non_blocking else ""
        p = Popen(args, stdout=PIPE, shell=True)

        (output, err) = p.communicate()

        p_status = p.wait()
        if err:
            raise PyMemucError(err)
        print(f"Command output [{p_status}]: {output}")
        return str(output)

    def get_version(self):
        self.run(["version"])

    def create_vm(self, vm_version="76"):
        self.run(["createvm", vm_version])

    def delete_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["deletevm", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["deletevm", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def clone_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["clonevm", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["clonevm", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def export_vm(
        self, vm_index=None, vm_name=None, file_name="vm.ova", non_blocking=False
    ):
        if vm_index is not None:
            self.run(["exportvm", "-i", str(vm_index), file_name], non_blocking)
        elif vm_name is not None:
            self.run(["exportvm", "-n", vm_name, file_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def import_vm(self, file_name="vm.ova", non_blocking=False):
        self.run(["importvm", file_name, "-t" if non_blocking else ""])

    def start_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        if vm_index is not None:
            self.run(["startvm", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            self.run(["startvm", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        if vm_index is not None:
            self.run(["stopvm", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            self.run(["stopvm", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_all_vm(self, non_blocking=False):
        self.run(["stopvm", "-a"], non_blocking)

    def list_vm_info(self, vm_index=None, vm_name=None, running=False, disk_info=False):
        # simulator index, title, top-level window handle, whether to start the simulator, process PID information, simulator disk usage
        if vm_index is not None:
            self.run(
                [
                    "listvms",
                    "-i",
                    str(vm_index),
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        elif vm_name is not None:
            self.run(
                [
                    "listvms",
                    "-n",
                    vm_name,
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        else:
            self.run(
                ["listvms", "-running" if running else "", "-s" if disk_info else ""]
            )

    def vm_is_running(self, vm_index=0):
        self.run(["isrunning", "-i", str(vm_index)])

    def sort_out_all_vm(self):
        self.run(["sortout"])

    def reboot_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        if vm_index is not None:
            self.run(["reboot", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            self.run(["reboot", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def rename_vm(self, vm_index=None, vm_name=None, new_name=None):
        if vm_index is not None:
            self.run(["renamevm", "-i", str(vm_index), f'"{new_name}"'])
        elif vm_name is not None:
            self.run(["renamevm", "-n", vm_name, f'"{new_name}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def check_task_status(self, task_id):
        self.run(["taskstatus", task_id])

    def get_configuration_vm(self, config_key, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["getconfig", "-i", str(vm_index), config_key])
        elif vm_name is not None:
            self.run(["getconfig", "-n", vm_name, config_key])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def set_configuration_vm(
        self, config_key, config_value, vm_index=None, vm_name=None
    ):
        if vm_index is not None:
            self.run(["setconfig", "-i", str(vm_index), config_key, config_value])
        elif vm_name is not None:
            self.run(["setconfig", "-n", vm_name, config_key, config_value])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def install_apk_vm(
        self, apk_path, vm_index=None, vm_name=None, create_shortcut=False
    ):
        if vm_index is not None:
            self.run(
                [
                    "installapk",
                    "-i",
                    str(vm_index),
                    apk_path,
                    "-s" if create_shortcut else "",
                ]
            )
        elif vm_name is not None:
            self.run(
                [
                    "installapk",
                    "-n",
                    vm_name,
                    apk_path,
                    "-s" if create_shortcut else "",
                ]
            )
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def uninstall_apk_vm(self, package_name, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["uninstallapk", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            self.run(["uninstallapk", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def start_app_vm(self, package_name, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["startapp", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            self.run(["startapp", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_app_vm(self, package_name, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["stopapp", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            self.run(["stopapp", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def trigger_keystroke_vm(
        self,
        key: Literal["back", "home", "menu", "volumeup", "volumedown"],
        vm_index=None,
        vm_name=None,
    ):
        if vm_index is not None:
            self.run(["triggerkey", "-i", str(vm_index), key])
        elif vm_name is not None:
            self.run(["triggerkey", "-n", vm_name, key])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def trigger_shake_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["triggershake", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["triggershake", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def connect_internet_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["connectinternet", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["connectinternet", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def disconnect_internet_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["disconnectinternet", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["disconnectinternet", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def input_text_vm(self, text, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["inputtext", "-i", str(vm_index), f'"{text}"'])
        elif vm_name is not None:
            self.run(["inputtext", "-n", vm_name, f'"{text}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def rotate_window_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["rotatewindow", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["rotatewindow", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def execute_command_vm(self, command, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["exec", "-i", str(vm_index), f'"{command}"'])
        elif vm_name is not None:
            self.run(["exec", "-n", vm_name, f'"{command}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def change_gps_vm(self, latitude, longitude, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["changegps", "-i", str(vm_index), str(latitude), str(longitude)])
        elif vm_name is not None:
            self.run(["changegps", "-n", vm_name, str(latitude), str(longitude)])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def get_public_ip_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            return self.run(
                ['execcmd "wget -O- whatismyip.akamai.com"', "-i", str(vm_index)]
            )
        elif vm_name is not None:
            return self.run(['execcmd "wget -O- whatismyip.akamai.com"', "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def zoom_in_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["zoomin", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["zoomin", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def zoom_out_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["zoomout", "-i", str(vm_index)])
        elif vm_name is not None:
            self.run(["zoomout", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def get_app_info_list_vm(self, vm_index=None, vm_name=None):
        if vm_index is not None:
            return self.run(["getappinfolist", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["getappinfolist", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def set_accelerometer_vm(
        self,
        x: float,
        y: float,
        z: float,
        vm_index=None,
        vm_name=None,
    ):
        if vm_index is not None:
            self.run(["setaccelerometer", "-i", str(vm_index), str(x), str(y), str(z)])
        elif vm_name is not None:
            self.run(["setaccelerometer", "-n", vm_name, str(x), str(y), str(z)])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def create_app_shortcut_vm(
        self,
        package_name: str,
        vm_index=None,
        vm_name=None,
    ):
        if vm_index is not None:
            self.run(["createappshortcut", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            self.run(["createappshortcut", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def send_adb_command_vm(self, command, vm_index=None, vm_name=None):
        if vm_index is not None:
            self.run(["sendadbcommand", "-i", str(vm_index), f'"{command}"'])
        elif vm_name is not None:
            self.run(["sendadbcommand", "-n", vm_name, f'"{command}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")


class PyMemucError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
