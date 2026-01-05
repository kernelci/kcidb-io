kcidb-io
========

`kcidb-io` is a Python 3 library for validating and manipulating Linux Kernel
CI reports in JSON format. This library is used by [`kcidb`][kcidb] - a
package for maintaining a service storing and serving that data.

Installation
------------

`kcidb-io` requires Python v3.10 or later.

To install the latest version from PyPI:

    pip3 install kcidb-io

To install from the git repository:

    pip3 install git+https://github.com/kernelci/kcidb-io.git

To install from a local directory:

    pip3 install .

Using
-----

Here's an example creating an empty report and then validating it:
```python
# Import the kcidb-io package
import kcidb_io
# Create an empty report using the latest schema version
json = kcidb_io.new()
# Validate the report
kcidb_io.schema.validate(json)
```

Hacking
-------

If you want to hack on the source code, install the package in the editable
mode with the `-e/--editable` option, and with "dev" extra included. E.g.:

    pip3 install --user --editable '.[dev]'

The latter installs the `kcidb-io` package using the modules from the source
directory, and changes to them will be reflected immediately without the need
to reinstall. It also installs extra development tools, such as `flake8` and
`pylint`.

[kcidb]: https://github.com/kernelci/kcidb/
