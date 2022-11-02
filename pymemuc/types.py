from typing import TypedDict


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
