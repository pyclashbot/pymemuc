# a wrapper for memuc.exe as a library to control virual machines
# documentation detailed in memuc_documentation.md

from os.path import abspath, expanduser, expandvars, join, normpath
from subprocess import PIPE, Popen
from typing import Literal

from pymemuc.types import VMInfo

try:
    from winreg import HKEY_LOCAL_MACHINE, ConnectRegistry, OpenKey, QueryValueEx

    windows_registry = True
except ImportError:
    print(
        "Windows Registry is not supported on this platform, you must specify the path to memuc.exe manually"
    )
    windows_registry = False


class PyMemuc:
    """A class to interact with the memuc.exe command line tool to control virtual machines.
    memuc.exe is automatically if windows registry is supported, otherwise a path must be specified.
    """

    def __init__(self, memuc_path=None) -> None:
        """initialize the class, automatically finding memuc.exe if windows registry is supported, otherwise a path must be specified

        Args:
            memuc_path (str, optional): Path to memuc.exe. Defaults to None.
        """
        if windows_registry:
            self.memuc_path = join(self.get_memu_top_level(), "memuc.exe")
        elif memuc_path is not None:
            raise PyMemucError(
                "Windows Registry is not supported on this platform, you must specify the path to memuc.exe manually"
            )
        else:
            self.memuc_path = memuc_path

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
                raise PyMemucError("MEmuc not found, is it installed?") from e
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
        p = Popen(args, stdout=PIPE, shell=False)

        (output, err) = p.communicate()
        output = output.decode("utf-8")  # convert bytes to string
        p_status = p.wait()
        if err:
            raise PyMemucError(err)
        # print(f"Command output [{p_status}]: {output}") # debug
        return p_status, output

    def create_vm(self, vm_version="76") -> int:
        """Create a new VM

        Args:
            vm_version (str, optional): Android version. Defaults to "76".

        Raises:
            PyMemucError: an error if the vm creation failed

        Returns:
            int: the index of the new VM, -1 if an error occurred but no exception was raised
        """
        status, output = self.run(["create", vm_version])
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to create VM: {output}")
        # filter out index from output eg "SUCCESS: create vm finished.index:100" -> 100
        return int(output.split(".")[-1]) if "." in output else -1

    def delete_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Delete a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            Literal[True]: True if the vm was deleted successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            Literal[True]: True if the vm was cloned successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            file_name (str, optional): File name. Defaults to "vm.ova".
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command
        """
        file_name = abspath(expandvars(expanduser(file_name)))
        if vm_index is not None:
            return self.run(
                ["-i", str(vm_index), "export", f'"{file_name}"'], non_blocking
            )
        elif vm_name is not None:
            return self.run(["-n", vm_name, "export", f'"{file_name}"'], non_blocking)
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def import_vm(self, file_name="vm.ova", non_blocking=False) -> Literal[True]:
        """Import a VM from a file

        Args:
            file_name (str, optional): File name. Defaults to "vm.ova".
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if the vm import failed

        Returns:
            Literal[True]: True if the vm was imported successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm start failed

        Returns:
            Literal[True]: True if the vm was started successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm stop failed

        Returns:
            Literal[True]: True if the vm was stopped successfully
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

        Args:
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucError: an error if the vm stop failed

        Returns:
            Literal[True]: True if the vm was stopped successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            running (bool, optional): Whether to list only running VMs. Defaults to False.
            disk_info (bool, optional): Whether to list disk info. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            list[vm_info]: a list of VM info, each VM info is a dictionary with the following keys:
                                    index: VM index
                                    title: VM title
                                    top_level: VM top level
                                    running: whether the VM is running
                                    pid: VM pid
                                    disk_usage: VM disk usage

        """

        if vm_index is not None:
            status, output = self.run(
                [
                    "-i",
                    str(vm_index),
                    "listvms",
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        elif vm_name is not None:
            status, output = self.run(
                [
                    "-n",
                    vm_name,
                    "listvms",
                    "-running" if running else "",
                    "-s" if disk_info else "",
                ]
            )
        else:
            status, output = self.run(
                ["listvms", "-running" if running else "", "-s" if disk_info else ""]
            )

        output = output.split("\r\n")
        parsed_output = []

        # parse the output into a list of dictionaries representing the VMs
        # output will contain a list of vm values seperated by commas, if disk_info is True, each vm will have 6 values, otherwise 5
        for vm in output:
            if vm:
                vm_info = vm.split(",")
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

        Args:
            vm_index (int, optional): VM index. Defaults to 0.

        Returns:
            bool: True if the VM is running, False otherwise
        """
        status, output = self.run(["-i", str(vm_index), "isrunning"])
        return "Running" in output

    def sort_out_all_vm(self) -> bool:
        """Sort out all VMs

        Returns:
            tuple[int, str]: the return code and the output of the command.
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            non_blocking (bool, optional): Whether to run the command in the background. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm reboot failed

        Returns:
            Literal[True]: True if the vm was rebooted successfully
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            new_name (str, optional): New VM name. Defaults to None.

        Raises:
            PyMemucError: an error if neither a vm index, name or new name is specified
            PyMemucError: an error if the vm rename failed

        Returns:
            Literal[True]: True if the vm was renamed successfully
        """
        if vm_index is not None and new_name is not None:
            status, output = self.run(["-i", str(vm_index), "rename", f'"{new_name}"'])
        elif vm_name is not None and new_name is not None:
            status, output = self.run(["-n", vm_name, "rename", f'"{new_name}"'])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        success = status == 0 and output is not None and "SUCCESS" in output
        if not success:
            raise PyMemucError(f"Failed to rename VM: {output}")
        return True

    # TODO: add output parsing
    def check_task_status(self, task_id):
        """Check the status of a task

        Args:
            task_id (str): Asynchronous task ID

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        return self.run("taskstatus", task_id)

    def get_configuration_vm(self, config_key, vm_index=None, vm_name=None) -> str:
        """Get a VM configuration, must specify either a vm index or a vm name

        Args:
            config_key (str): Configuration key, keys are noted in docs/memuc_documentation.md
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm configuration failed

        Returns:
            str: The configuration value
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

        Args:
            config_key (str): Configuration key, keys are noted in docs/memuc_documentation.md
            config_value (str): Configuration value
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm configuration failed

        Returns:
            Literal[True]: True if the vm configuration was set successfully
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

        Args:
            apk_path (str): Path to the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.
            create_shortcut (bool, optional): Whether to create a shortcut. Defaults to False.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm apk installation failed

        Returns:
            Literal[True]: True if the vm apk installation was successful
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

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm apk uninstallation failed

        Returns:
            Literal[True]: True if the vm apk uninstallation was successful
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

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm app start failed

        Returns:
            Literal[True]: True if the vm app start was successful
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

        Args:
            package_name (str): Package name of the APK
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm app stop failed

        Returns:
            Literal[True]: True if the vm app stop was successful
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

        Args:
            key (Literal["back", "home", "menu", "volumeup", "volumedown"]): Key to trigger
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm keystroke trigger failed

        Returns:
            Literal[True]: True if the vm keystroke trigger was successful
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm shake trigger failed

        Returns:
            Literal[True]: True if the vm shake trigger was successful
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm internet connection failed

        Returns:
            Literal[True]: True if the vm internet connection was successful
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

    def disconnect_internet_vm(self, vm_index=None, vm_name=None):
        """Disconnect the internet on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
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

        Args:
            text (str): Text to input
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm text input failed

        Returns:
            Literal[True]: True if the vm text input was successful
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm window rotation failed

        Returns:
            Literal[True]: True if the vm window rotation was successful
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

        Args:
            command (str): Command to execute
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "execcmd", f'"{command}"'])
        elif vm_name is not None:
            return self.run(["-n", vm_name, "execcmd", f'"{command}"'])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def change_gps_vm(
        self, latitude: float, longitude: float, vm_index=None, vm_name=None
    ) -> Literal[True]:
        """Change the GPS location on a VM, must specify either a vm index or a vm name

        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm GPS change failed

        Returns:
            Literal[True]: True if the vm GPS change was successful
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
    def get_public_ip_vm(self, vm_index=None, vm_name=None):
        """Get the public IP of a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ["-i", str(vm_index), 'execcmd "wget -O- whatismyip.akamai.com"']
            )
        elif vm_name is not None:
            return self.run(["-n", vm_name, 'execcmd "wget -O- whatismyip.akamai.com"'])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")

    def zoom_in_vm(self, vm_index=None, vm_name=None) -> Literal[True]:
        """Zoom in on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm zoom in failed

        Returns:
            Literal[True]: True if the vm zoom in was successful
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

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified
            PyMemucError: an error if the vm zoom out failed

        Returns:
            Literal[True]: True if the vm zoom out was successful
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

    def get_app_info_list_vm(self, vm_index=None, vm_name=None) -> list[str]:
        """Get the list of apps installed on a VM, must specify either a vm index or a vm name

        Args:
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            list[str]: the list of packages installed on the VM
        """
        if vm_index is not None:
            status, output = self.run(["-i", str(vm_index), "getappinfolist"])
        elif vm_name is not None:
            status, output = self.run(["-n", vm_name, "getappinfolist"])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")
        output = output.split("\r\n")
        output = [line.replace("package:", "") for line in output if line != ""]
        return output

    # TODO: debug this, it doesn't work
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
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(
                ["-i", str(vm_index), "accelerometer", str(x), str(y), str(z)]
            )
        elif vm_name is not None:
            return self.run(["-n", vm_name, "accelerometer", str(), str(y), str(z)])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")

    # TODO: functionally works, but hangs after the command is run
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
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "createshortcut", package_name])
        elif vm_name is not None:
            return self.run(["-n", vm_name, "createshortcut", package_name])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")

    # TODO: parse the output
    def send_adb_command_vm(self, command, vm_index=None, vm_name=None):
        """Send an ADB command to a VM, must specify either a vm index or a vm name

        Args:
            command (str): ADB command
            vm_index (int, optional): VM index. Defaults to None.
            vm_name (str, optional): VM name. Defaults to None.

        Raises:
            PyMemucIndexError: an error if neither a vm index or a vm name is specified

        Returns:
            tuple[int, str]: the return code and the output of the command.
        """
        if vm_index is not None:
            return self.run(["-i", str(vm_index), "adb", f'"{command}"'])
        elif vm_name is not None:
            return self.run(["-n", vm_name, "adb", f'"{command}"'])
        else:
            raise PyMemucIndexError("Please specify either a vm index or a vm name")


class PyMemucError(Exception):
    """PyMemuc error class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PyMemucIndexError(PyMemucError):
    """PyMemuc index error class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
