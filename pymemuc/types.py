"""A type definition for VM info"""

from typing import Literal, TypedDict


class VMInfo(TypedDict):
    """A TypedDict for VM info"""

    index: int
    """ VM index """
    title: str
    """VM title"""
    top_level: str
    """VM top level window"""
    running: bool
    """VM is running"""
    pid: int
    """VM process ID"""
    disk_usage: int
    """VM disk usage in bytes"""


class ConfigKeys(TypedDict):
    name: str
    cpus: str
    cpucap: str
    memory: str
    is_full_screen: Literal[1, 0]
    is_hide_toolbar: Literal[1, 0]
    turbo_mode: Literal[1, 0]
    graphics_render_mode: Literal[1, 0]
    enable_su: Literal[1, 0]
    enable_audio: Literal[1, 0]
    fps: str
    virtual_keyboard_mode: Literal[0, 1]
    sync_time: Literal[1, 0]
    phone_layout: Literal[2, 1, 0]
    start_window_mode: Literal[2, 1, 0]
    win_x: str
    win_y: str
    win_scaling_percent2: str
    is_custom_resolution: Literal[1, 0]
    resolution_width: str
    resolution_height: str
    vbox_dpi: str
    linenum: str
    imei: str
    imsi: str
    simserial: str
    microvirt_vm_brand: str
    microvirt_vm_model: str
    microvirt_vm_manufacturer: str
    selected_map: Literal[0, 1]
    latitude: str
    longitude: str
    picturepath: str
    musicpath: str
    moviepath: str
    downloadpath: str
