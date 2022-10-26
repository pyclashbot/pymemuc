# a wrapper for memuc.exe as a library to control virual machines
# documentation detailed in memuc_documentation.md

from subprocess import Popen, PIPE
from os.path import join, normpath
from typing import Literal
from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx


class PyMemuc:
    """A class to interact with the memuc.exe command line tool to control virtual machines"""

    def __init__(self) -> None:
        """initialize the class, automatically finding memuc.exe"""
        self.memuc_path = join(self.get_memu_top_level(), "memuc.exe")

    def get_memu_top_level(self) -> str:
        """locate the path of the memu directory using windows registry keys

        Returns:
            str: the path of the memu directory
        """
        try:
            akey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MEmu"
            areg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            akey = OpenKey(areg, akey)
        except FileNotFoundError:
            try:
                akey = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\MEmu"
                areg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                akey = OpenKey(areg, akey)
            except FileNotFoundError as e:
                raise PyMemucError("MEmu not found") from e
        return str(join(normpath(QueryValueEx(akey, "InstallLocation")[0]), "Memu"))

    def run(self, args, non_blocking=False) -> tuple[int, str]:
        """run a command with memuc.exe

        Args:
            args (list): a list of arguments to pass to memuc.exe
            non_blocking (bool, optional): whether to run the command in the background. Defaults to False.

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        args.insert(0, self.memuc_path)
        args += "-t" if non_blocking else ""
        p = Popen(args, stdout=PIPE, shell=True)

        (output, err) = p.communicate()
        output = output.decode("utf-8").replace("\r", "").replace("\n", "")
        p_status = p.wait()
        if err:
            raise PyMemucError(err)
        print(f"Command output [{p_status}]: {output}")
        return p_status, output

    def create_vm(self, vm_version="76"):
        """Create a new VM

        Args:
            vm_version (str, optional): Android version. Defaults to "76".

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        return self.run(["createvm", vm_version])

    def delete_vm(self, vm_index=None, vm_name=None):
        """Delete a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        if vm_index is not None:
            return self.run(["deletevm", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["deletevm", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def clone_vm(self, vm_index=None, vm_name=None):
        """Clone a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        if vm_index is not None:
            return self.run(["clonevm", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["clonevm", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def export_vm(
        self, vm_index=None, vm_name=None, file_name="vm.ova", non_blocking=False
    ):
        """Export a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            file_name (str, optional): File name. Defaults to "vm.ova".
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        if vm_index is not None:
            return self.run(["exportvm", "-i", str(vm_index), file_name], non_blocking)
        elif vm_name is not None:
            return self.run(["exportvm", "-n", vm_name, file_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def import_vm(self, file_name="vm.ova", non_blocking=False):
        """Import a VM from a file

        Args:
            file_name (str, optional): File name. Defaults to "vm.ova".
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        return self.run(["importvm", file_name, "-t" if non_blocking else ""])

    def start_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        """Start a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        if vm_index is not None:
            return self.run(["startvm", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            return self.run(["startvm", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        """Stop a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        if vm_index is not None:
            return self.run(["stopvm", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            return self.run(["stopvm", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_all_vm(self, non_blocking=False):
        """Stop all VMs

        Args:
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        return self.run(["stopvm", "-a"], non_blocking)

    def list_vm_info(self, vm_index=None, vm_name=None, running=False, disk_info=False):
        """List VM info, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            running (bool, optional): Whether to list only running VMs. Defaults to False.
            disk_info (bool, optional): Whether to list disk info. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command. output contains simulator index, title, top-level window handle, whether to start the simulator, process PID information, simulator disk usage

        """

        if vm_index is not None:
            return self.run(
                [
                    "listvms",
                    "-i",
                    str(vm_index),
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        elif vm_name is not None:
            return self.run(
                [
                    "listvms",
                    "-n",
                    vm_name,
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        else:
            return self.run(
                ["listvms", "-running" if running else "", "-s" if disk_info else ""]
            )

    def vm_is_running(self, vm_index=0):
        """Check if a VM is running

        Args:
            vm_index (int, optional): VM index. Defaults to 0.

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        return self.run(["isrunning", "-i", str(vm_index)])

    def sort_out_all_vm(self):
        """Sort out all VMs

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        return self.run(["sortout"])

    def reboot_vm(self, vm_index=None, vm_name=None, non_blocking=False):
        """Reboot a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["reboot", "-i", str(vm_index)], non_blocking)
        elif vm_name is not None:
            return self.run(["reboot", "-n", vm_name], non_blocking)
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def rename_vm(self, vm_index=None, vm_name=None, new_name=None):
        """Rename a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            new_name (str, optional): New VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index, name or new name is specified"""
        if vm_index is not None and new_name is not None:
            return self.run(["renamevm", "-i", str(vm_index), f'"{new_name}"'])
        elif vm_name is not None and new_name is not None:
            return self.run(["renamevm", "-n", vm_name, f'"{new_name}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def check_task_status(self, task_id):
        """Check the status of a task

        Args:
            task_id (str): Asynchronous task ID

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        return self.run(["taskstatus", task_id])

    def get_configuration_vm(self, config_key, vm_index=None, vm_name=None):
        """Get a VM configuration, must specify either a vm index or a vm name

        Args:
            config_key (str): Configuration key, keys are noted in docs/memuc_documentation.md
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["getconfig", "-i", str(vm_index), config_key])
        elif vm_name is not None:
            return self.run(["getconfig", "-n", vm_name, config_key])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def set_configuration_vm(
        self, config_key, config_value, vm_index=None, vm_name=None
    ):
        """Set a VM configuration, must specify either a vm index or a vm name

        Args:
            config_key (str): Configuration key, keys are noted in docs/memuc_documentation.md
            config_value (str): Configuration value
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ["setconfig", "-i", str(vm_index), config_key, config_value]
            )
        elif vm_name is not None:
            return self.run(["setconfig", "-n", vm_name, config_key, config_value])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def install_apk_vm(
        self, apk_path, vm_index=None, vm_name=None, create_shortcut=False
    ):
        """Install an APK on a VM, must specify either a vm index or a vm name

        Args:
            apk_path (str): Path to the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            create_shortcut (bool, optional): Whether to create a shortcut. Defaults to False.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                [
                    "installapk",
                    "-i",
                    str(vm_index),
                    apk_path,
                    "-s" if create_shortcut else "",
                ]
            )
        elif vm_name is not None:
            return self.run(
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
        """Uninstall an APK on a VM, must specify either a vm index or a vm name

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["uninstallapk", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            return self.run(["uninstallapk", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def start_app_vm(self, package_name, vm_index=None, vm_name=None):
        """Start an app on a VM, must specify either a vm index or a vm name

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["startapp", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            return self.run(["startapp", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def stop_app_vm(self, package_name, vm_index=None, vm_name=None):
        """Stop an app on a VM, must specify either a vm index or a vm name

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["stopapp", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            return self.run(["stopapp", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def trigger_keystroke_vm(
        self,
        key: Literal["back", "home", "menu", "volumeup", "volumedown"],
        vm_index=None,
        vm_name=None,
    ):
        """Trigger a keystroke on a VM, must specify either a vm index or a vm name

        Args:
            key (Literal["back", "home", "menu", "volumeup", "volumedown"]): Key to trigger
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["triggerkey", "-i", str(vm_index), key])
        elif vm_name is not None:
            return self.run(["triggerkey", "-n", vm_name, key])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def trigger_shake_vm(self, vm_index=None, vm_name=None):
        """Trigger a shake on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["triggershake", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["triggershake", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def connect_internet_vm(self, vm_index=None, vm_name=None):
        """Connect the internet on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["connectinternet", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["connectinternet", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def disconnect_internet_vm(self, vm_index=None, vm_name=None):
        """Disconnect the internet on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["disconnectinternet", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["disconnectinternet", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def input_text_vm(self, text, vm_index=None, vm_name=None):
        """Input text on a VM, must specify either a vm index or a vm name

        Args:
            text (str): Text to input
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["inputtext", "-i", str(vm_index), f'"{text}"'])
        elif vm_name is not None:
            return self.run(["inputtext", "-n", vm_name, f'"{text}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def rotate_window_vm(self, vm_index=None, vm_name=None):
        """Rotate the window on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["rotatewindow", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["rotatewindow", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def execute_command_vm(self, command, vm_index=None, vm_name=None):
        """Execute a command on a VM, must specify either a vm index or a vm name

        Args:
            command (str): Command to execute
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["exec", "-i", str(vm_index), f'"{command}"'])
        elif vm_name is not None:
            return self.run(["exec", "-n", vm_name, f'"{command}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def change_gps_vm(self, latitude:float, longitude:float, vm_index=None, vm_name=None):
        """Change the GPS location on a VM, must specify either a vm index or a vm name

        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ["changegps", "-i", str(vm_index), str(latitude), str(longitude)]
            )
        elif vm_name is not None:
            return self.run(["changegps", "-n", vm_name, str(latitude), str(longitude)])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def get_public_ip_vm(self, vm_index=None, vm_name=None):
        """Get the public IP of a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ['execcmd "wget -O- whatismyip.akamai.com"', "-i", str(vm_index)]
            )
        elif vm_name is not None:
            return self.run(['execcmd "wget -O- whatismyip.akamai.com"', "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def zoom_in_vm(self, vm_index=None, vm_name=None):
        """Zoom in on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["zoomin", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["zoomin", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def zoom_out_vm(self, vm_index=None, vm_name=None):
        """Zoom out on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["zoomout", "-i", str(vm_index)])
        elif vm_name is not None:
            return self.run(["zoomout", "-n", vm_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def get_app_info_list_vm(self, vm_index=None, vm_name=None):
        """Get the list of apps installed on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
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
        """Set the accelerometer on a VM, must specify either a vm index or a vm name

        Args:
            x (float): X value
            y (float): Y value
            z (float): Z value
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ["setaccelerometer", "-i", str(vm_index), str(x), str(y), str(z)]
            )
        elif vm_name is not None:
            return self.run(["setaccelerometer", "-n", vm_name, str(x), str(y), str(z)])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def create_app_shortcut_vm(
        self,
        package_name: str,
        vm_index=None,
        vm_name=None,
    ):
        """Create an app shortcut on a VM, must specify either a vm index or a vm name

        Args:
            package_name (str): Package name
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["createappshortcut", "-i", str(vm_index), package_name])
        elif vm_name is not None:
            return self.run(["createappshortcut", "-n", vm_name, package_name])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")

    def send_adb_command_vm(self, command, vm_index=None, vm_name=None):
        """Send an ADB command to a VM, must specify either a vm index or a vm name

        Args:
            command (str): ADB command
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["sendadbcommand", "-i", str(vm_index), f'"{command}"'])
        elif vm_name is not None:
            return self.run(["sendadbcommand", "-n", vm_name, f'"{command}"'])
        else:
            raise PyMemucError("Please specify either a vm index or a vm name")


class PyMemucError(Exception):
    """PyMemuc error class"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
