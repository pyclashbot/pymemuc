"""a wrapper for memuc.exe as a library to control virual machines"""

from os.path import join
from typing import Union

from ._constants import WINREG_EN
from .exceptions import PyMemucError


class PyMemuc:
    """A class to interact with the memuc.exe command line tool to control virtual machines.

    :param memuc_path: Path to memuc.exe. Set to None for autodetect.
    :type memuc_path: str, optional
    :param debug: Enable debug mode, defaults to False
    :type debug: bool, optional
    """

    # pylint: disable=import-outside-toplevel

    from ._command import (
        change_gps_vm,
        connect_internet_vm,
        create_app_shortcut_vm,
        disconnect_internet_vm,
        execute_command_vm,
        get_app_info_list_vm,
        get_public_ip_vm,
        input_text_vm,
        install_apk_vm,
        rotate_window_vm,
        send_adb_command_vm,
        set_accelerometer_vm,
        sort_out_all_vm,
        start_app_vm,
        stop_app_vm,
        trigger_keystroke_vm,
        trigger_shake_vm,
        uninstall_apk_vm,
        zoom_in_vm,
        zoom_out_vm,
    )
    from ._control import reboot_vm, start_vm, stop_all_vm, stop_vm
    from ._manage import (
        clone_vm,
        create_vm,
        delete_vm,
        export_vm,
        get_configuration_vm,
        import_vm,
        list_vm_info,
        rename_vm,
        set_configuration_vm,
        vm_is_running,
    )
    from ._memuc import _get_memu_top_level, check_task_status, memuc_run

    def __init__(self, memuc_path: Union[str, None] = None, debug=False) -> None:
        """initialize the class, automatically finding memuc.exe if windows registry is supported,
        otherwise a path must be specified"""
        self.debug = debug
        if self.debug:
            print("PyMemuc: Debug mode enabled")
        if WINREG_EN:
            self.memuc_path: str = join(self._get_memu_top_level(), "memuc.exe")
        elif memuc_path is not None:
            self.memuc_path: str = memuc_path
        else:
            raise PyMemucError(
                "Windows Registry is not supported on this platform, you must specify the path to memuc.exe manually"
            )
