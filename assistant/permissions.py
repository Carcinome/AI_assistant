"""
Defines constants for simple capabilities within a system.

The module provides predefined capability constants that can
be used to manage and check permissions or functionalities
within a given application or service.
"""


from typing import Dict


# Simples capabilities.
READ_FS = "read_fs"
WRITE_FS = "write_fs"
USE_CALC = "use_calc"
USE_TIMER = "use_timer"

DEFAULT_PERMISSIONS: Dict[str, bool] = {
    READ_FS: False,
    WRITE_FS: False,
    USE_CALC: True,
    USE_TIMER: True,
    # Calculs and timers allowed by default.
}

def is_allowed(perms: Dict[str, bool], capability: str) -> bool:
    return bool(perms.get(capability, False))