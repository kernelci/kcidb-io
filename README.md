kcidb-io
========

`kcidb-io` is a Python 3 library for validating and manipulating Linux Kernel
CI reports in JSON format. This library is used by [`kcidb`][kcidb] - a
package for maintaining a service storing and serving that data.

Installation
------------

`kcidb-io` requires Python v3.6 or later.

To install the package for the current user, run this command:

    pip3 install --user <SOURCE>

Where `<SOURCE>` is the location of the package source, e.g. a git repo:

    pip3 install --user git+https://github.com/kernelci/kcidb-io.git

or a directory path:

    pip3 install --user .

In any case, make sure your PATH includes the `~/.local/bin` directory, e.g.
with:

    export PATH="$PATH":~/.local/bin

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

Releasing
---------

Before releasing make sure the README.md is up to date.

To make a release tag the release commit with `v<NUMBER>`, where `<NUMBER>` is
the next release number, e.g. `v1`. The very next commit after the tag should
update the version number in `setup.py` to be the next one. I.e. continuing
the above example, it should be `2`.

[kcidb]: https://github.com/kernelci/kcidb/
