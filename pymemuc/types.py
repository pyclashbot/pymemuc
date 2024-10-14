"""Type definitions for pymemuc."""

from typing import Literal, TypedDict


class VMInfo(TypedDict):
    """A TypedDict for VM info."""

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


ConfigKeys = Literal[
    "name",
    "cpus",
    "cpucap",
    "memory",
    "is_full_screen",
    "is_hide_toolbar",
    "turbo_mode",
    "graphics_render_mode",
    "enable_su",
    "enable_audio",
    "fps",
    "vkeyboard_mode",
    "sync_time",
    "phone_layout",
    "start_window_mode",
    "win_x",
    "win_y",
    "win_scaling_percent2",
    "is_customed_resolution",
    "resolution_width",
    "resolution_height",
    "vbox_dpi",
    "linenum",
    "imei",
    "imsi",
    "simserial",
    "microvirt_vm_brand",
    "microvirt_vm_model",
    "microvirt_vm_manufacturer",
    "selected_map",
    "latitude",
    "longitude",
    "picturepath",
    "musicpath",
    "moviepath",
    "downloadpath",
    "macaddress",
    "cache_mode",
    "geometry",
    "custom_resolution",
    "disable_resize",
    "ssid",
]
