"""a wrapper for memuc.exe as a library to control virual machines"""
import re
from os import environ
from os.path import abspath, expanduser, expandvars, join, normpath
from subprocess import PIPE, CalledProcessError, Popen, TimeoutExpired, check_output
from typing import Literal, Union

from pymemuc.exceptions import PyMemucError, PyMemucIndexError, PyMemucTimeoutExpired
from pymemuc.vminfo import VMInfo

# check for windows registry support
try:
    from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx

    WINREG_EN = True
except ImportError:
    print(
        "Windows Registry is not supported on this platform, "
        + "you must specify the path to memuc.exe manually"
    )
    WINREG_EN = False

# check for debug mode
environment = environ.get("PYTHON_ENV", "development")
DEBUG = environment == "development"

if __name__ == "__main__" and DEBUG:
    print("Debug mode enabled")  # debug


class PyMemuc:
    """A class to interact with the memuc.exe command line tool to control virtual machines.

    :param memuc_path: Path to memuc.exe. Set to None for autodetect.
    :type memuc_path: str, optional
    """

    def __init__(self, memuc_path: Union[str, None] = None) -> None:
        """initialize the class, automatically finding memuc.exe if windows registry is supported,
        otherwise a path must be specified"""
        if WINREG_EN:
            self.memuc_path: str = join(self._get_memu_top_level(), "memuc.exe")
        elif memuc_path is None:
            raise PyMemucError(
                "Windows Registry is not supported on this platform, "
                + "you must specify the path to memuc.exe manually"
            )
        else:
            self.memuc_path: str = memuc_path

    def _get_memu_top_level(self) -> str:
        """locate the path of the memu directory using windows registry keys

        :return: the path of the memu directory
        :rtype: str
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
            except FileNotFoundError as err:
                raise PyMemucError("MEmuc not found, is it installed?") from err
        return str(join(normpath(QueryValueEx(akey, "InstallLocation")[0]), "Memu"))

    def run(self, args: list[str], non_blocking=False) -> tuple[int, str]:
        """run a command with memuc.exe

        :param args: a list of arguments to pass to memuc.exe
        :type args: list[str]
        :param non_blocking: whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :return: the return code and the output of the command
        :rtype: tuple[int, str]
        :raises PyMemucError: an error if the command failed
        """
        args.insert(0, self.memuc_path)
        args += "-t" if non_blocking else ""
        with Popen(args, stdout=PIPE, shell=False) as proc:
            (output, err) = proc.communicate()
            output = output.decode("utf-8")  # convert bytes to string
            p_status = proc.wait()
            if err:
                raise PyMemucError(err)

            if DEBUG:
                # print the command that was run and the output for debugging
                print(f"Command: memuc.exe {' '.join(args)}")  # debug
                print(f"Command output [{p_status}]: {output}")  # debug

            return p_status, output

    def run_with_timeout(self, args: list[str], timeout=10) -> tuple[int, str]:
        """run a command with memuc.exe with a timeout

        :param args: a list of arguments to pass to memuc.exe
        :type args: list[str]
        :param timeout: the timeout in seconds. Defaults to 10.
        :type timeout: int, optional
        :return: the return code and the output of the command
        :rtype: tuple[int, str]
        :raises PyMemucError: an error if the command failed
        :raises PyMemucTimeoutExpired: an error if the command timed out
        """
        args.insert(0, self.memuc_path)
        try:
            output = check_output(args, timeout=timeout)
            return (1, output.decode("utf-8"))
        except CalledProcessError as err:
            raise PyMemucError(err) from err
        except TimeoutExpired as err:
            raise PyMemucTimeoutExpired(err) from err

    def create_vm(self, vm_version="76") -> int:
        """Create a new VM

        :param vm_version: Android version. Defaults to "76".
        :type vm_version: str, optional
        :raises PyMemucError: an error if the vm creation failed
        :return: the index of the new VM, -1 if an error occurred but no exception was raised
        :rtype: int
        """
        status, output = self.run(["create", vm_version])
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to create VM: {output}")
        # filter output with regex r"index:(\w)"
        try:
            indecies = re.search(r"index:(\w)", output)
            return -1 if indecies is None else int(indecies[1])
        except AttributeError:
            return -1

    def delete_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Delete a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm was deleted successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "remove"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "remove"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to delete VM: {output}")
        return True

    def clone_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Clone a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm was cloned successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "clone"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "clone"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to clone VM: {output}")
        return True

    # TODO: verify functionality
    def export_vm(
        self, vm_index=None, vm_name=None, file_name="vm.ova", non_blocking=False
    ):
        """Export a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param file_name: File name. Defaults to "vm.ova".
        :type file_name: str, optional
        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command
        :rtype: tuple[int, str]
        """
        file_name = abspath(expandvars(expanduser(file_name)))
        if vm_index is not None:
            return self.run(
                ["-i", str(vm_index), "export", f'"{file_name}"'], non_blocking
            )
        if vm_name is not None:
            return self.run(["-n", vm_name, "export", f'"{file_name}"'], non_blocking)
        raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def import_vm(self, file_name="vm.ova", non_blocking=False) -> Literal[True]:
        """Import a VM from a file

        :param file_name: File name. Defaults to "vm.ova".
        :type file_name: str, optional
        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucError: an error if the vm import failed
        :return: True if the vm was imported successfully
        :rtype: Literal[True]
        """
        status, output = self.run(["import", file_name], non_blocking)
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to import VM: {output}")
        return True

    def start_vm(
        self, vm_index=None, vm_name=None, non_blocking=False
    ) -> Literal[True]:
        """Start a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm was started successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "start"], non_blocking)
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "start"], non_blocking)
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to start VM: {output}")
        return True

    def stop_vm(self, vm_index=None, vm_name=None, non_blocking=False) -> Literal[True]:
        """Stop a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm was stopped successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "stop"], non_blocking)
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "stop"], non_blocking)
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to stop VM: {output}")
        return True

    def stop_all_vm(self, non_blocking=False) -> Literal[True]:
        """Stop all VMs

        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucError: an error if the vm stop failed
        :return: True if the vm was stopped successfully
        :rtype: Literal[True]
        """
        status, output = self.run(["stopall"], non_blocking)
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to stop all VMs: {output}")
        return True

    def list_vm_info(
        self, vm_index=None, vm_name=None, running=False, disk_info=False
    ) -> list[VMInfo]:
        """List VM info, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param running: Whether to list only running VMs. Defaults to False.
        :type running: bool, optional
        :param disk_info: Whether to list disk info. Defaults to False.
        :type disk_info: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: a list of VM info, each VM info is a dictionary with the following keys:
                                    index: VM index
                                    title: VM title
                                    top_level: VM top level
                                    running: whether the VM is running
                                    pid: VM pid
                                    disk_usage: VM disk usage
        :rtype: list[VMInfo]
        """

        if vm_index is not None:
            _, output = self.run(
                [
                    "-i",
                    str(vm_index),
                    "listvms",
                    "-r" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        elif vm_name is not None:
            _, output = self.run(
                [
                    "-n",
                    vm_name,
                    "listvms",
                    "-r" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        else:
            _, output = self.run(
                ["listvms", "-r" if running else "", "-s" if disk_info else ""]
            )

        output = output.split("\r\n")
        parsed_output = []

        # parse the output into a list of dictionaries representing the VMs
        # output will contain a list of vm values seperated by commas
        # if disk_info is True, each vm will have 6 values, otherwise 5
        for vm_str in output:
            if vm_str:
                vm_info = vm_str.split(",")
                parsed_output.append(
                    {
                        "index": int(vm_info[0]),
                        "title": vm_info[1],
                        "top_level": vm_info[2],
                        "running": vm_info[3] == "1",
                        "pid": int(vm_info[4]),
                        "disk_usage": int(vm_info[5]) if disk_info else -1,
                    }
                )
        return parsed_output

    def vm_is_running(self, vm_index=0) -> bool:
        """Check if a VM is running

        :param vm_index: VM index. Defaults to 0.
        :type vm_index: int, optional
        :return: True if the VM is running, False otherwise
        :rtype: bool
        """
        _, output = self.run(["-i", str(vm_index), "isrunning"])
        return "Running" in output

    def sort_out_all_vm(self) -> bool:
        """Sort out all VMs

        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        status, output = self.run(["sortwin"])
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to sort out all VMs: {output}")
        return True

    def reboot_vm(
        self, vm_index=None, vm_name=None, non_blocking=False
    ) -> Literal[True]:
        """Reboot a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param non_blocking: Whether to run the command in the background. Defaults to False.
        :type non_blocking: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm was rebooted successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "reboot"], non_blocking)
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "reboot"], non_blocking)
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to reboot VM: {output}")
        return True

    def rename_vm(self, vm_index=None, vm_name=None, new_name=None) -> Literal[True]:
        """Rename a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param new_name: New VM name. Defaults to None.
        :type new_name: str, optional
        :raises PyMemucError: an error if neither a vm index, name or new name is specified
        :return: True if the vm was renamed successfully
        :rtype: Literal[True]
        """
        if vm_index is not None and new_name is not None:
            status, output = self.run(["-i", str(vm_index), "rename", new_name])
        elif vm_name is not None and new_name is not None:
            status, output = self.run(["-n", vm_name, "rename", new_name])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to rename VM: {output}")
        return True

    # TODO: add output parsing
    def check_task_status(self, task_id):
        """Check the status of a task

        :param task_id: Asynchronous task ID
        :type task_id: str
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        return self.run(["taskstatus"], task_id)

    def get_configuration_vm(self, config_key, vm_index=None, vm_name=None) -> str:
        """Get a VM configuration, must specify either a vm index or a vm name

        :param config_key: Configuration key, keys are noted in `configuration keys table <https://pymemuc.readthedocs.io/pymemuc.html#the-vm-configuration-keys-table>`_
        :type config_key: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: The configuration value
        :rtype: str
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "getconfigex", config_key])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "getconfigex", config_key])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "Value" in output
        if not success:
            raise PyMemucError(f"Failed to get VM configuration: {output}")
        return output.split("Value: ")[1].replace("\n", "").replace("\r", "")

    def set_configuration_vm(
        self, config_key: str, config_value: str, vm_index=None, vm_name=None
    ) -> Literal[True]:
        """Set a VM configuration, must specify either a vm index or a vm name

        :param config_key: Configuration key, keys are noted in `configuration keys table <https://pymemuc.readthedocs.io/pymemuc.html#the-vm-configuration-keys-table>`_
        :type config_key: str
        :param config_value: Configuration value
        :type config_value: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm configuration was set successfully
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(
                ["-i", str(vm_index), "setconfigex", config_key, config_value]
            )
        elif vm_name is not None:
            status, output = self.run(
                ["-n", vm_name, "setconfigex", config_key, config_value]
            )
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to set VM configuration: {output}")
        return True

    # TODO: look into bindings with https://github.com/egirault/googleplay-api
    def install_apk_vm(
        self, apk_path, vm_index=None, vm_name=None, create_shortcut=False
    ) -> Literal[True]:
        """Install an APK on a VM, must specify either a vm index or a vm name

        :param apk_path: Path to the APK
        :type apk_path: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param create_shortcut: Whether to create a shortcut. Defaults to False.
        :type create_shortcut: bool, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm apk installation was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(
                [
                    "installapp",
                    "-i",
                    str(vm_index),
                    apk_path,
                    "-s" if create_shortcut else "",
                ]
            )
        elif vm_name is not None:
            status, output = self.run(
                [
                    "installapp",
                    "-n",
                    vm_name,
                    apk_path,
                    "-s" if create_shortcut else "",
                ]
            )
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to install APK: {output}")
        return True

    def uninstall_apk_vm(
        self, package_name, vm_index=None, vm_name=None
    ) -> Literal[True]:
        """Uninstall an APK on a VM, must specify either a vm index or a vm name

        :param package_name: Package name of the APK
        :type package_name: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm apk uninstallation was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(
                ["-i", str(vm_index), "uninstallapp", package_name]
            )
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "uninstallapp", package_name])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to uninstall APK: {output}")
        return True

    def start_app_vm(self, package_name, vm_index=None, vm_name=None) -> Literal[True]:
        """Start an app on a VM, must specify either a vm index or a vm name

        :param package_name: Package name of the APK
        :type package_name: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm app start was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "startapp", package_name])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "startapp", package_name])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to start app: {output}")
        return True

    def stop_app_vm(self, package_name, vm_index=None, vm_name=None) -> Literal[True]:
        """Stop an app on a VM, must specify either a vm index or a vm name

        :param package_name: Package name of the APK
        :type package_name: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm app stop was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "stopapp", package_name])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "stopapp", package_name])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to stop app: {output}")
        return True

    def trigger_keystroke_vm(
        self,
        key: Literal["back", "home", "menu", "volumeup", "volumedown"],
        vm_index=None,
        vm_name=None,
    ) -> Literal[True]:
        """Trigger a keystroke on a VM, must specify either a vm index or a vm name

        :param key: Key to trigger
        :type key: Literal["back", "home", "menu", "volumeup", "volumedown"]
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm keystroke trigger was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "sendkey", key])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "sendkey", key])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to trigger keystroke: {output}")
        return True

    def trigger_shake_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Trigger a shake on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm shake trigger was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "shake"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "shake"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to trigger shake: {output}")
        return True

    def connect_internet_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Connect the internet on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm internet connection was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "connect"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "connect"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to connect internet: {output}")
        return True

    def disconnect_internet_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Disconnect the internet on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "disconnect"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "disconnect"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to disconnect internet: {output}")
        return True

    def input_text_vm(self, text, vm_index=None, vm_name=None) -> Literal[True]:
        """Input text on a VM, must specify either a vm index or a vm name

        :param text: Text to input
        :type text: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm text input was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "input", text])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "input", text])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to input text: {output}")
        return True

    def rotate_window_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Rotate the window on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm window rotation was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "rotate"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "rotate"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to rotate window: {output}")
        return True

    def execute_command_vm(
        self, command, vm_index=None, vm_name=None
    ) -> tuple[int, str]:
        """Execute a command on a VM, must specify either a vm index or a vm name

        :param command: Command to execute
        :type command: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "execcmd", f'"{command}"'])
        if vm_name is not None:
            return self.run(["-n", vm_name, "execcmd", f'"{command}"'])
        raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def change_gps_vm(
        self, latitude: float, longitude: float, vm_index=None, vm_name=None
    ) -> Literal[True]:
        """Change the GPS location on a VM, must specify either a vm index or a vm name

        :param latitude: Latitude
        :type latitude: float
        :param longitude: Longitude
        :type longitude: float
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm GPS change was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            success, output = self.run(
                ["-i", str(vm_index), "setgps", str(latitude), str(longitude)]
            )
        elif vm_name is not None:
            success, output = self.run(
                ["-n", vm_name, "setgps", str(latitude), str(longitude)]
            )
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = success == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to change GPS location: {output}")
        return True

    # TODO: fix parsing of the output
    def get_public_ip_vm(self, vm_index=None, vm_name=None) -> tuple[int, str]:
        """Get the public IP of a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        if vm_index is not None:
            return self.run(
                ["-i", str(vm_index), 'execcmd "wget -O- whatismyip.akamai.com"']
            )
        if vm_name is not None:
            return self.run(["-n", vm_name, 'execcmd "wget -O- whatismyip.akamai.com"'])
        raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def zoom_in_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Zoom in on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm zoom in was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "zoomin"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "zoomin"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to zoom in: {output}")
        return True

    def zoom_out_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Zoom out on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: True if the vm zoom out was successful
        :rtype: Literal[True]
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "zoomout"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "zoomout"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to zoom in: {output}")
        return True

    def get_app_info_list_vm(
        self, vm_index=None, vm_name=None, timeout=10
    ) -> list[str]:
        """Get the list of apps installed on a VM, must specify either a vm index or a vm name

        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :param timeout: Timeout for the command. Defaults to 10.
        :type timeout: int, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the list of packages installed on the VM
        :rtype: list[str]
        """
        try:
            if vm_index is not None:
                _, output = self.run_with_timeout(
                    ["-i", str(vm_index), "getappinfolist"],
                    timeout=timeout,
                )
            elif vm_name is not None:
                _, output = self.run_with_timeout(
                    ["-n", vm_name, "getappinfolist"],
                    timeout=timeout,
                )
            else:
                raise PyMemucIndexError("Please specify either a vm index or a vm name")
            output = output.split("\r\n")
            output = [line.replace("package:", "") for line in output if line != ""]
            return output
        except PyMemucTimeoutExpired:
            return []

    # TODO: debug this, it doesn't work
    def set_accelerometer_vm(
        self,
        value: tuple[float, float, float],
        vm_index=None,
        vm_name=None,
    ) -> tuple[int, str]:
        """Set the accelerometer on a VM, must specify either a vm index or a vm name

        :param value: the accelerometer value to set
        :type value: tuple[float, float, float]
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """

        if vm_index is not None:
            return self.run(
                [
                    "-i",
                    str(vm_index),
                    "accelerometer",
                    str(value[0]),
                    str(value[1]),
                    str(value[2]),
                ]
            )
        if vm_name is not None:
            return self.run(
                [
                    "-n",
                    vm_name,
                    "accelerometer",
                    str(value[0]),
                    str(value[1]),
                    str(value[2]),
                ]
            )
        raise PyMemucIndexError("Please specify either a vm index or a vm name")

    # TODO: functionally works, but hangs after the command is run
    def create_app_shortcut_vm(
        self,
        package_name: str,
        vm_index=None,
        vm_name=None,
    ) -> tuple[int, str]:
        """Create an app shortcut on a VM, must specify either a vm index or a vm name

        :param package_name: Package name
        :type package_name: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "createshortcut", package_name])
        if vm_name is not None:
            return self.run(["-n", vm_name, "createshortcut", package_name])
        raise PyMemucIndexError("Please specify either a vm index or a vm name")

    # TODO: parse the output
    def send_adb_command_vm(
        self, command, vm_index=None, vm_name=None
    ) -> tuple[int, str]:
        """Send an ADB command to a VM, must specify either a vm index or a vm name

        :param command: ADB command
        :type command: str
        :param vm_index: VM index. Defaults to None.
        :type vm_index: int, optional
        :param vm_name: VM name. Defaults to None.
        :type vm_name: str, optional
        :raises PyMemucIndexError: an error if neither a vm index or a vm name is specified
        :return: the return code and the output of the command.
        :rtype: tuple[int, str]
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "adb", f'"{command}"'])
        if vm_name is not None:
            return self.run(["-n", vm_name, "adb", f'"{command}"'])
        raise PyMemucIndexError("Please specify either a vm index or a vm name")
