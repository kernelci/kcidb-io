"""Kernel CI reporting I/O data - misc definitions"""

import os

# Check light assertions only, if True
LIGHT_ASSERTS = not os.environ.get("KCIDB_IO_HEAVY_ASSERTS", "")
