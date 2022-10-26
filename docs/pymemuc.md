# Table of Contents

- [pymemuc](#pymemuc)
- [pymemuc.\_\_main\_\_](#pymemuc.__main__)
  - [PyMemuc](#pymemuc.__main__.PyMemuc)
    - [\_\_init\_\_](#pymemuc.__main__.PyMemuc.__init__)
    - [get_memu_top_level](#pymemuc.__main__.PyMemuc.get_memu_top_level)
    - [run](#pymemuc.__main__.PyMemuc.run)
    - [create_vm](#pymemuc.__main__.PyMemuc.create_vm)
    - [delete_vm](#pymemuc.__main__.PyMemuc.delete_vm)
    - [clone_vm](#pymemuc.__main__.PyMemuc.clone_vm)
    - [export_vm](#pymemuc.__main__.PyMemuc.export_vm)
    - [import_vm](#pymemuc.__main__.PyMemuc.import_vm)
    - [start_vm](#pymemuc.__main__.PyMemuc.start_vm)
    - [stop_vm](#pymemuc.__main__.PyMemuc.stop_vm)
    - [stop_all_vm](#pymemuc.__main__.PyMemuc.stop_all_vm)
    - [list_vm_info](#pymemuc.__main__.PyMemuc.list_vm_info)
    - [vm_is_running](#pymemuc.__main__.PyMemuc.vm_is_running)
    - [sort_out_all_vm](#pymemuc.__main__.PyMemuc.sort_out_all_vm)
    - [reboot_vm](#pymemuc.__main__.PyMemuc.reboot_vm)
    - [rename_vm](#pymemuc.__main__.PyMemuc.rename_vm)
    - [check_task_status](#pymemuc.__main__.PyMemuc.check_task_status)
    - [get_configuration_vm](#pymemuc.__main__.PyMemuc.get_configuration_vm)
    - [set_configuration_vm](#pymemuc.__main__.PyMemuc.set_configuration_vm)
    - [install_apk_vm](#pymemuc.__main__.PyMemuc.install_apk_vm)
    - [uninstall_apk_vm](#pymemuc.__main__.PyMemuc.uninstall_apk_vm)
    - [start_app_vm](#pymemuc.__main__.PyMemuc.start_app_vm)
    - [stop_app_vm](#pymemuc.__main__.PyMemuc.stop_app_vm)
    - [trigger_keystroke_vm](#pymemuc.__main__.PyMemuc.trigger_keystroke_vm)
    - [trigger_shake_vm](#pymemuc.__main__.PyMemuc.trigger_shake_vm)
    - [connect_internet_vm](#pymemuc.__main__.PyMemuc.connect_internet_vm)
    - [disconnect_internet_vm](#pymemuc.__main__.PyMemuc.disconnect_internet_vm)
    - [input_text_vm](#pymemuc.__main__.PyMemuc.input_text_vm)
    - [rotate_window_vm](#pymemuc.__main__.PyMemuc.rotate_window_vm)
    - [execute_command_vm](#pymemuc.__main__.PyMemuc.execute_command_vm)
    - [change_gps_vm](#pymemuc.__main__.PyMemuc.change_gps_vm)
    - [get_public_ip_vm](#pymemuc.__main__.PyMemuc.get_public_ip_vm)
    - [zoom_in_vm](#pymemuc.__main__.PyMemuc.zoom_in_vm)
    - [zoom_out_vm](#pymemuc.__main__.PyMemuc.zoom_out_vm)
    - [get_app_info_list_vm](#pymemuc.__main__.PyMemuc.get_app_info_list_vm)
    - [set_accelerometer_vm](#pymemuc.__main__.PyMemuc.set_accelerometer_vm)
    - [create_app_shortcut_vm](#pymemuc.__main__.PyMemuc.create_app_shortcut_vm)
    - [send_adb_command_vm](#pymemuc.__main__.PyMemuc.send_adb_command_vm)
  - [PyMemucError](#pymemuc.__main__.PyMemucError)

<a id="pymemuc"></a>

# pymemuc

<a id="pymemuc.__main__"></a>

# pymemuc.\_\_main\_\_

<a id="pymemuc.__main__.PyMemuc"></a>

## PyMemuc Objects

```python
class PyMemuc()
```

A class to interact with the memuc.exe command line tool to control virtual machines

<a id="pymemuc.__main__.PyMemuc.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

initialize the class, automatically finding memuc.exe

<a id="pymemuc.__main__.PyMemuc.get_memu_top_level"></a>

#### get_memu_top_level

```python
def get_memu_top_level() -> str
```

locate the path of the memu directory using windows registry keys

**Returns**:

- `str` - the path of the memu directory

<a id="pymemuc.__main__.PyMemuc.run"></a>

#### run

```python
def run(args, non_blocking=False) -> tuple[int, str]
```

run a command with memuc.exe

**Arguments**:

- `args` _list_ - a list of arguments to pass to memuc.exe
- `non_blocking` _bool, optional_ - whether to run the command in the background. Defaults to False.

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.create_vm"></a>

#### create_vm

```python
def create_vm(vm_version="76")
```

Create a new VM

**Arguments**:

- `vm_version` _str, optional_ - Android version. Defaults to "76".

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.delete_vm"></a>

#### delete_vm

```python
def delete_vm(vm_index=None, vm_name=None)
```

Delete a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.clone_vm"></a>

#### clone_vm

```python
def clone_vm(vm_index=None, vm_name=None)
```

Clone a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.export_vm"></a>

#### export_vm

```python
def export_vm(vm_index=None,
              vm_name=None,
              file_name="vm.ova",
              non_blocking=False)
```

Export a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `file_name` _str, optional_ - File name. Defaults to "vm.ova".
- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.import_vm"></a>

#### import_vm

```python
def import_vm(file_name="vm.ova", non_blocking=False)
```

Import a VM from a file

**Arguments**:

- `file_name` _str, optional_ - File name. Defaults to "vm.ova".
- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.start_vm"></a>

#### start_vm

```python
def start_vm(vm_index=None, vm_name=None, non_blocking=False)
```

Start a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.stop_vm"></a>

#### stop_vm

```python
def stop_vm(vm_index=None, vm_name=None, non_blocking=False)
```

Stop a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.stop_all_vm"></a>

#### stop_all_vm

```python
def stop_all_vm(non_blocking=False)
```

Stop all VMs

**Arguments**:

- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Returns**:

tuple[int, str]: the return code and the output of the command

<a id="pymemuc.__main__.PyMemuc.list_vm_info"></a>

#### list_vm_info

```python
def list_vm_info(vm_index=None, vm_name=None, running=False, disk_info=False)
```

List VM info, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `running` _bool, optional_ - Whether to list only running VMs. Defaults to False.
- `disk_info` _bool, optional_ - Whether to list disk info. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command. output contains simulator index, title, top-level window handle, whether to start the simulator, process PID information, simulator disk usage

<a id="pymemuc.__main__.PyMemuc.vm_is_running"></a>

#### vm_is_running

```python
def vm_is_running(vm_index=0)
```

Check if a VM is running

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to 0.

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.sort_out_all_vm"></a>

#### sort_out_all_vm

```python
def sort_out_all_vm()
```

Sort out all VMs

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.reboot_vm"></a>

#### reboot_vm

```python
def reboot_vm(vm_index=None, vm_name=None, non_blocking=False)
```

Reboot a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `non_blocking` _bool, optional_ - Whether to run the command in the background. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.rename_vm"></a>

#### rename_vm

```python
def rename_vm(vm_index=None, vm_name=None, new_name=None)
```

Rename a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `new_name` _str, optional_ - New VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index, name or new name is specified

<a id="pymemuc.__main__.PyMemuc.check_task_status"></a>

#### check_task_status

```python
def check_task_status(task_id)
```

Check the status of a task

**Arguments**:

- `task_id` _str_ - Asynchronous task ID

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.get_configuration_vm"></a>

#### get_configuration_vm

```python
def get_configuration_vm(config_key, vm_index=None, vm_name=None)
```

Get a VM configuration, must specify either a vm index or a vm name

**Arguments**:

- `config_key` _str_ - Configuration key, keys are noted in docs/memuc_documentation.md
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.set_configuration_vm"></a>

#### set_configuration_vm

```python
def set_configuration_vm(config_key,
                         config_value,
                         vm_index=None,
                         vm_name=None)
```

Set a VM configuration, must specify either a vm index or a vm name

**Arguments**:

- `config_key` _str_ - Configuration key, keys are noted in docs/memuc_documentation.md
- `config_value` _str_ - Configuration value
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.install_apk_vm"></a>

#### install_apk_vm

```python
def install_apk_vm(apk_path,
                   vm_index=None,
                   vm_name=None,
                   create_shortcut=False)
```

Install an APK on a VM, must specify either a vm index or a vm name

**Arguments**:

- `apk_path` _str_ - Path to the APK
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.
- `create_shortcut` _bool, optional_ - Whether to create a shortcut. Defaults to False.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.uninstall_apk_vm"></a>

#### uninstall_apk_vm

```python
def uninstall_apk_vm(package_name, vm_index=None, vm_name=None)
```

Uninstall an APK on a VM, must specify either a vm index or a vm name

**Arguments**:

- `package_name` _str_ - Package name of the APK
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.start_app_vm"></a>

#### start_app_vm

```python
def start_app_vm(package_name, vm_index=None, vm_name=None)
```

Start an app on a VM, must specify either a vm index or a vm name

**Arguments**:

- `package_name` _str_ - Package name of the APK
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.stop_app_vm"></a>

#### stop_app_vm

```python
def stop_app_vm(package_name, vm_index=None, vm_name=None)
```

Stop an app on a VM, must specify either a vm index or a vm name

**Arguments**:

- `package_name` _str_ - Package name of the APK
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.trigger_keystroke_vm"></a>

#### trigger_keystroke_vm

```python
def trigger_keystroke_vm(key: Literal["back", "home", "menu", "volumeup",
                                      "volumedown"],
                         vm_index=None,
                         vm_name=None)
```

Trigger a keystroke on a VM, must specify either a vm index or a vm name

**Arguments**:

- `key` _Literal["back", "home", "menu", "volumeup", "volumedown"]_ - Key to trigger
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.trigger_shake_vm"></a>

#### trigger_shake_vm

```python
def trigger_shake_vm(vm_index=None, vm_name=None)
```

Trigger a shake on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.connect_internet_vm"></a>

#### connect_internet_vm

```python
def connect_internet_vm(vm_index=None, vm_name=None)
```

Connect the internet on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.disconnect_internet_vm"></a>

#### disconnect_internet_vm

```python
def disconnect_internet_vm(vm_index=None, vm_name=None)
```

Disconnect the internet on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.input_text_vm"></a>

#### input_text_vm

```python
def input_text_vm(text, vm_index=None, vm_name=None)
```

Input text on a VM, must specify either a vm index or a vm name

**Arguments**:

- `text` _str_ - Text to input
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.rotate_window_vm"></a>

#### rotate_window_vm

```python
def rotate_window_vm(vm_index=None, vm_name=None)
```

Rotate the window on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.execute_command_vm"></a>

#### execute_command_vm

```python
def execute_command_vm(command, vm_index=None, vm_name=None)
```

Execute a command on a VM, must specify either a vm index or a vm name

**Arguments**:

- `command` _str_ - Command to execute
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.change_gps_vm"></a>

#### change_gps_vm

```python
def change_gps_vm(latitude: float,
                  longitude: float,
                  vm_index=None,
                  vm_name=None)
```

Change the GPS location on a VM, must specify either a vm index or a vm name

**Arguments**:

- `latitude` _float_ - Latitude
- `longitude` _float_ - Longitude
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.get_public_ip_vm"></a>

#### get_public_ip_vm

```python
def get_public_ip_vm(vm_index=None, vm_name=None)
```

Get the public IP of a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.zoom_in_vm"></a>

#### zoom_in_vm

```python
def zoom_in_vm(vm_index=None, vm_name=None)
```

Zoom in on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.zoom_out_vm"></a>

#### zoom_out_vm

```python
def zoom_out_vm(vm_index=None, vm_name=None)
```

Zoom out on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.get_app_info_list_vm"></a>

#### get_app_info_list_vm

```python
def get_app_info_list_vm(vm_index=None, vm_name=None)
```

Get the list of apps installed on a VM, must specify either a vm index or a vm name

**Arguments**:

- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.set_accelerometer_vm"></a>

#### set_accelerometer_vm

```python
def set_accelerometer_vm(x: float,
                         y: float,
                         z: float,
                         vm_index=None,
                         vm_name=None)
```

Set the accelerometer on a VM, must specify either a vm index or a vm name

**Arguments**:

- `x` _float_ - X value
- `y` _float_ - Y value
- `z` _float_ - Z value
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.create_app_shortcut_vm"></a>

#### create_app_shortcut_vm

```python
def create_app_shortcut_vm(package_name: str, vm_index=None, vm_name=None)
```

Create an app shortcut on a VM, must specify either a vm index or a vm name

**Arguments**:

- `package_name` _str_ - Package name
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemuc.send_adb_command_vm"></a>

#### send_adb_command_vm

```python
def send_adb_command_vm(command, vm_index=None, vm_name=None)
```

Send an ADB command to a VM, must specify either a vm index or a vm name

**Arguments**:

- `command` _str_ - ADB command
- `vm_index` _int, optional_ - VM index. Defaults to None.
- `vm_name` _str, optional_ - VM name. Defaults to None.

**Raises**:

- `PyMemucError` - an error if neither a vm index or a vm name is specified

**Returns**:

tuple[int, str]: the return code and the output of the command.

<a id="pymemuc.__main__.PyMemucError"></a>

## PyMemucError Objects

```python
class PyMemucError(Exception)
```

PyMemuc error class
