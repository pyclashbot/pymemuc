"""Tests for VM management helpers."""
# ruff: noqa: PT009

from __future__ import annotations

import unittest

from pymemuc import PyMemuc
from pymemuc._manage import set_configuration_vm


class FakeMemuc(PyMemuc):
    """Minimal PyMemuc test double that records generated memuc commands."""

    def __init__(self) -> None:
        """Create a fake command runner."""
        self.commands: list[list[str]] = []

    def memuc_run(self, command: list[str]) -> tuple[int, str]:
        """Record the command and report a successful memuc invocation."""
        self.commands.append(command)
        return 0, "SUCCESS: setconfig finished.\n"


class SetConfigurationVmTests(unittest.TestCase):
    """Tests for set_configuration_vm command generation."""

    def test_custom_resolution_is_passed_as_three_memuc_arguments(self) -> None:
        """custom_resolution must not be passed as one quoted value."""
        memuc = FakeMemuc()

        result = set_configuration_vm(
            memuc,
            "custom_resolution",
            "270 480 120",
            vm_index=0,
        )

        self.assertTrue(result)
        self.assertEqual(
            memuc.commands,
            [["-i", "0", "setconfigex", "custom_resolution", "270", "480", "120"]],
        )

    def test_single_value_config_preserves_spaces_as_one_argument(self) -> None:
        """Single-value config keys should continue preserving spaces."""
        memuc = FakeMemuc()

        set_configuration_vm(memuc, "name", "My VM", vm_name="phone")

        self.assertEqual(
            memuc.commands,
            [["-n", "phone", "setconfigex", "name", "My VM"]],
        )


if __name__ == "__main__":
    unittest.main()
