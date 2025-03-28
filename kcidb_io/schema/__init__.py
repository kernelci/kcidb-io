"""Kernel CI reporting I/O schema"""
from kcidb_io.schema.abstract import Version as VA  # noqa: F401
from kcidb_io.schema.v01_01 import Version as V1_1  # noqa: F401
from kcidb_io.schema.v02_00 import Version as V2_0  # noqa: F401
from kcidb_io.schema.v03_00 import Version as V3_0  # noqa: F401
from kcidb_io.schema.v04_00 import Version as V4_0  # noqa: F401
from kcidb_io.schema.v04_01 import Version as V4_1  # noqa: F401
from kcidb_io.schema.v04_02 import Version as V4_2  # noqa: F401
from kcidb_io.schema.v04_03 import Version as V4_3  # noqa: F401
from kcidb_io.schema.v04_04 import Version as V4_4  # noqa: F401
from kcidb_io.schema.v04_05 import Version as V4_5  # noqa: F401
from kcidb_io.schema.v05_00 import Version as V5_0  # noqa: F401
from kcidb_io.schema.v05_01 import Version as V5_1  # noqa: F401
from kcidb_io.schema.v05_02 import Version as V5_2  # noqa: F401
from kcidb_io.schema.v05_03 import Version as V5_3  # noqa: F401

# Legacy versions
V1 = V1_1  # noqa: F401
V2 = V2_0  # noqa: F401
V3 = V3_0  # noqa: F401
V4 = V4_0  # noqa: F401

# Latest version of the schema
LATEST = V5_3
