"""Kernel CI reporting I/O schema v4"""

from kcidb_io.schema.v3 import Version as PreviousVersion


class Version(PreviousVersion):
    """Version"""

    # Major version number of the schema.
    major = PreviousVersion.major + 1

    # Minor version number of the schema.
    minor = 0

    # JSON schema for I/O data
    json = {
        "title": "kcidb",
        "description":
            "Kernel CI report data. To be submitted to/queried from the "
            "common report database.\n"
            "\n"
            "Objects in the data are identified and linked together using "
            "\"id\" and \"*_id\" string properties. Each value of these "
            "properties must start with a non-empty string identifying the "
            "CI system which submitted the object, followed by a colon ':' "
            "character. The rest of the string is generated by the origin "
            "CI system, and must identify that object uniquely among all "
            "objects of the same type, coming from that CI system.\n"
            "\n"
            "Any of the immediate properties (except \"version\") can be "
            "missing or be an empty list with each submission/query, but "
            "only complete data stored in the database should be considered "
            "valid.\n"
            "\n"
            "E.g. a test run referring to a non-existent build is allowed "
            "into/from the database, but would only appear in reports once "
            "both the build and its source code checkout are present.\n"
            "\n"
            "No special meaning apart from \"data is missing\" is attached to "
            "any immediate or deeper properties being omitted, when they're "
            "not required, and no default values should be assumed for them. "
            "At the same time, no properties can be null.\n"
            "\n"
            "Extra free-form data can be stored under \"misc\" fields "
            "associated with various objects throughout the schema, if "
            "necessary. That data could later be used as the basis for "
            "defining new properties to house it.",
        "type": "object",

        "$defs": {
            # A named remote resource
            "resource": {
                "title": "resource",
                "description": "A named remote resource",
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description":
                            "Resource name. Must be usable as a local file "
                            "name for the downloaded resource. Cannot be "
                            "empty. Should not include directories.",
                        "pattern": "^[^/]+$",
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "Resource URL. Must point to the resource "
                            "file directly, so it could be downloaded "
                            "automatically.",
                    },
                },
                "additionalProperties": False,
                "required": ["name", "url"],
                "examples": [
                    {
                        "name": "console.log",
                        "url":
                            "https://artifacts.cki-project.org/pipelines/"
                            "223563/logs/aarch64_host_1_console.log"
                    },
                    {
                        "name": "kernel.tar.gz",
                        "url":
                            "https://artifacts.cki-project.org/pipelines/"
                            "224569/kernel-stable-aarch64-"
                            "a2fc8ee6676067f27d2f5c6e4d512adff3d9938c.tar.gz"
                    }
                ]
            },

            # A list of named remote resources
            "resource_list": {
                "type": "array",
                "description": "A list of named remote resources",
                "items": {"$ref": "#/$defs/resource"},
            },

            # A source code checkout being tested
            "checkout": {
                "title": "checkout",
                "description":
                    "The source code checkout being tested.\n"
                    "\n"
                    "Represents the way the tested source code was obtained "
                    "and its original location. E.g. checking out a"
                    " particular commit from a git "
                    "repo, and applying a set of patches on top.\n"
                    "\n"
                    "There could be multiple checkouts of the same source "
                    "code location, and multiple locations for the same "
                    "code revision. Such as multiple checkouts "
                    "of the same commit appearing in multiple "
                    "Git repos, or "
                    "multiple downloads and applications "
                    "of the same patchset sent to "
                    "multiple maillists.\n",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description":
                            "Source code checkout ID\n"
                            "\n"
                            "Must start with a non-empty string identifying"
                            " the CI system which submitted the checkout, "
                            "followed by a colon ':' character. The rest of "
                            "the string is generated by the "
                            "origin CI system, and must identify the checkout"
                            " uniquely among all checkouts, coming from "
                            "that CI system.\n",
                        "pattern": f"^{PreviousVersion.origin_id_pattern}$",
                    },
                    "origin": {
                        "type": "string",
                        "description":
                            "The name of the CI system which submitted "
                            "the checkout",
                        "pattern": f"^{PreviousVersion.origin_pattern}$",
                    },
                    "tree_name": {
                        "type": "string",
                        "description":
                            "The widely-recognized name of the sub-tree "
                            "(fork) of the main code tree where the checked "
                            "out base source code came from.",
                        "examples": [
                            "net-next",
                            "rdma",
                            "mainline",
                        ],
                    },
                    "git_repository_url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "The URL of the Git repository which contains the "
                            "checked out base source code. The shortest "
                            "possible https:// URL, or, if that's not "
                            "available, the shortest possible git:// URL.",
                        "pattern":
                            f"^{PreviousVersion.git_repository_url_pattern}$",
                        "examples": [
                            "https://git.kernel.org/pub/scm/linux/kernel/git/"
                            "torvalds/linux.git",
                        ],
                    },
                    "git_commit_hash": {
                        "type": "string",
                        "description":
                            "The full commit hash of the checked out base "
                            "source code",
                        "pattern":
                            f"^{PreviousVersion.git_commit_hash_pattern}$",
                    },
                    "git_commit_name": {
                        "type": "string",
                        "description":
                            "A human-readable name of the commit containing "
                            "the checked out base source code, as would be "
                            "output by \"git describe\", at the checkout time."
                    },
                    "git_repository_branch": {
                        "type": "string",
                        "description":
                            "The Git repository branch from which the commit "
                            "with the base source code was checked out."
                    },
                    "patchset_files": {
                        "description":
                            "List of patch files representing the patchset "
                            "applied to the checked out base source code, "
                            "in order of application. Each linked file must "
                            "be in a format accepted by \"git apply\".",
                        "$ref": "#/$defs/resource_list"
                    },
                    "patchset_hash": {
                        "type": "string",
                        "description":
                            "The patchset hash.\n"
                            "\n"
                            "A sha256 hash over newline-terminated sha256 "
                            "hashes of each patch from the patchset, in "
                            "order. E.g. generated with this shell command: "
                            "\"sha256sum *.patch | cut -c-64 | sha256sum | "
                            "cut -c-64\".\n"
                            "\n"
                            "An empty string, if no patches were applied to "
                            "the checked out base source code.\n",
                        "pattern": f"^$|^{PreviousVersion.sha256_pattern}$",
                        "examples": [
                            "",
                            "903638c087335b10293663c682b9aa0076f9f7be478a8"
                            "e7828bc22e12d301b42"
                        ],
                    },
                    "message_id": {
                        "type": "string",
                        "format": "email",
                        "description":
                            "The value of the Message-ID header of the e-mail "
                            "message introducing the checked-out source code, "
                            "if any. E.g. a message with the applied "
                            "patchset, or a release announcement sent to a "
                            "maillist.",
                    },
                    "comment": {
                        "type": "string",
                        "description":
                            "A human-readable comment regarding the checkout. "
                            "E.g. the checked out release version, or the "
                            "subject of the message with the applied patchset."
                    },
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description":
                            "The time the checkout was started.",
                        "examples": [
                            "2020-08-14T23:08:06.967000+00:00",
                        ],
                    },
                    "contacts": {
                        "type": "array",
                        "description":
                            "List of e-mail addresses of contacts concerned "
                            "with the checked out source code, such as "
                            "authors, reviewers, and mail lists",
                        "items": {
                            "type": "string",
                            "description":
                                "An e-mail address of a contact concerned "
                                "with this code, e.g. an author, a reviewer, "
                                "or a mail list, as in "
                                "https://tools.ietf.org/html/rfc5322"
                                "#section-3.4"
                        },
                    },
                    "log_url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "The URL of a plain-text log file of the "
                            "checkout attempt. "
                            "E.g. 'git am' output.",
                    },
                    "log_excerpt": {
                        "type": "string",
                        "maxLength": 16384,
                        "description":
                            "A part of the log file of the checkout attempt "
                            "most relevant to its outcome.",
                        "examples": [
                            "error: patch failed: "
                            "arch/arm64/boot/dts/qcom/sc7180.dtsi:510\n"
                            "error: arch/arm64/boot/dts/qcom/sc7180.dtsi: "
                            "patch does not apply\n",
                        ],
                    },
                    "valid": {
                        "type": "boolean",
                        "description":
                            "True if the checkout succeeded, i.e. if the "
                            "source code parts could be combined. False if "
                            "not, e.g. if the patches failed to apply."
                    },
                    "misc": {
                        "type": "object",
                        "description":
                            "Miscellaneous extra data about the checkout",
                    },
                },
                "additionalProperties": False,
                "required": [
                    "id",
                    "origin",
                ],
            },

            # A build of a source code checkout
            "build": {
                "title": "build",
                "description": "A build of a source code checkout",
                "type": "object",
                "properties": {
                    "checkout_id": {
                        "type": "string",
                        "description":
                            "ID of the built source code checkout. The "
                            "checkout must be valid for the build to be "
                            "considered valid.",
                        "pattern": f"^{PreviousVersion.origin_id_pattern}$",
                    },
                    "id": {
                        "type": "string",
                        "description":
                            "Build ID\n"
                            "\n"
                            "Must start with a non-empty string identifying "
                            "the CI system which submitted the build, "
                            "followed by a colon ':' character. The "
                            "rest of the string is generated by the origin "
                            "CI system, and must identify the build uniquely "
                            "among all builds, coming from that CI system.\n",
                        "pattern": f"^{PreviousVersion.origin_id_pattern}$",
                    },
                    "origin": {
                        "type": "string",
                        "description":
                            "The name of the CI system which submitted the "
                            "build",
                        "pattern": f"^{PreviousVersion.origin_pattern}$",
                    },
                    "comment": {
                        "type": "string",
                        "description":
                            "A human-readable comment regarding the build"
                    },
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description":
                            "The time the build was started",
                        "examples": [
                            "2020-08-14T23:08:06.967000+00:00",
                        ],
                    },
                    "duration": {
                        "type": "number",
                        "description":
                            "The number of seconds it took to complete the "
                            "build",
                    },
                    "architecture": {
                        "type": "string",
                        "description":
                            "Target architecture of the build",
                        "pattern": "^[a-z0-9_]*$"
                    },
                    "command": {
                        "type": "string",
                        "description":
                            "Full shell command line used to make the build, "
                            "including environment variables",
                    },
                    "compiler": {
                        "type": "string",
                        "description":
                            "Name and version of the compiler used to "
                            "make the build",
                    },
                    "input_files": {
                        "description":
                            "A list of build input files. E.g. configuration.",
                        "$ref": "#/$defs/resource_list"
                    },
                    "output_files": {
                        "description":
                            "A list of build output files: images, packages, "
                            "etc.",
                        "$ref": "#/$defs/resource_list"
                    },
                    "config_name": {
                        "type": "string",
                        "description":
                            "A name describing the build configuration "
                            "options.",
                    },
                    "config_url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "The URL of the build configuration file.",
                    },
                    "log_url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "The URL of the plain-text build log file.",
                    },
                    "log_excerpt": {
                        "type": "string",
                        "maxLength": 16384,
                        "description":
                            "A part of the log file of the build most "
                            "relevant to its "
                            "outcome.",
                        "examples": [
                            "In file included from "
                            "./arch/arm64/include/asm/processor.h:35:\n"
                            "./arch/arm64/include/asm/pointer_auth.h:62:3: "
                            "error: invalid input constraint 'rZ' in asm\n"
                            "                __ptrauth_key_install(APIA, "
                            "keys->apia);\n                ^\n"
                            "./arch/arm64/include/asm/pointer_auth.h:55:2: "
                            "note: expanded from macro "
                            "'__ptrauth_key_install'\n"
                            "        write_sysreg_s(__pki_v.lo, "
                            "SYS_ ## k ## KEYLO_EL1);     \\\n"
                            "        ^\n./arch/arm64/include/asm/sysreg.h:"
                            "829:37:"
                            " note: expanded from macro 'write_sysreg_s'\n"
                            "        asm volatile(__msr_s(r, \"%x0\") : : "
                            "\"rZ\" (__val));               \\\n"
                            "                                           ^\n"
                        ],
                    },
                    "valid": {
                        "type": "boolean",
                        "description":
                            "True if the build is valid, i.e. if it could"
                            " be completed. False if not.",
                    },
                    "misc": {
                        "type": "object",
                        "description":
                            "Miscellaneous extra data about the build",
                    },
                },
                "additionalProperties": False,
                "required": ["checkout_id", "id", "origin"],
            },

            # A test run on a build
            "test": {
                "title": "test",
                "description":
                    "A test run against a build.\n"
                    "\n"
                    "Could represent a result of execution of a test "
                    "suite program, a result of one of the tests done by "
                    "the test suite program, as well as a summary of a "
                    "collection of test suite results.\n"
                    "\n"
                    "Each test run should normally have a dot-separated "
                    "test \"path\" specified in the \"path\" property, "
                    "which could identify a specific test within a "
                    "test suite (e.g. \"LTPlite.sem01\"), a whole test "
                    "suite (e.g. \"LTPlite\"), or the summary "
                    "of all tests for a build "
                    "("" - the empty string).",
                "type": "object",
                "properties": {
                    "build_id": {
                        "type": "string",
                        "description":
                            "ID of the tested build. The build must be "
                            "valid for the test run to be considered valid.",
                        "pattern": f"^{PreviousVersion.origin_id_pattern}$",
                    },
                    "id": {
                        "type": "string",
                        "description":
                            "ID of the test run\n"
                            "\n"
                            "Must start with a non-empty string identifying "
                            "the CI system which submitted the test run, "
                            "followed by a colon ':' character. "
                            "The rest of the string is generated by the "
                            "origin CI system, and must identify the test "
                            "run uniquely among all test runs, coming from "
                            "that CI system.\n",
                        "pattern": f"^{PreviousVersion.origin_id_pattern}$",
                    },
                    "origin": {
                        "type": "string",
                        "description":
                            "The name of the CI system which submitted the"
                            " test run",
                        "pattern": f"^{PreviousVersion.origin_pattern}$",
                    },
                    "environment": {
                        "type": "object",
                        "description":
                            "The environment the test ran in. "
                            "E.g. a host, a set of hosts, or a lab; "
                            "amount of memory/storage/CPUs, for each host; "
                            "process environment variables, etc.",
                        "properties": {
                            "comment": {
                                "type": "string",
                                "description":
                                    "A human-readable comment regarding the "
                                    "environment."
                            },
                            "misc": {
                                "type": "object",
                                "description":
                                    "Miscellaneous extra data about the "
                                    "environment",
                            },
                        },
                        "additionalProperties": False,
                    },
                    "path": {
                        "type": "string",
                        "description":
                            "Dot-separated path to the node in the test "
                            "classification tree the executed test belongs to."
                            " E.g. \"ltp.sem01\". The empty string signifies"
                            " the root of the tree, i.e. all tests for "
                            "the build, executed by the origin CI system.",
                        "pattern": "^[.a-zA-Z0-9_-]*$",
                        "examples": [
                            "",
                            "ltp",
                            "ltp.sem01",
                        ],
                    },
                    "comment": {
                        "type": "string",
                        "description":
                            "A human-readable comment regarding the test run"
                    },
                    "log_url": {
                        "type": "string",
                        "format": "uri",
                        "description":
                            "The URL of the plain-text test output or log "
                            "file. If the test produced multiple "
                            "outputs/files, this should point to the one "
                            "containing the highest-level overview of the "
                            "test's operation. The rest should go into "
                            "\"output_files\"."
                    },
                    "log_excerpt": {
                        "type": "string",
                        "maxLength": 16384,
                        "description":
                            "A part of the test output/log file "
                            "(which could be) referenced by \"log_url\", "
                            "most relevant to the test outcome.",
                        "examples": [
                            "netns_breakns_ns_exec_ipv4_ioctl FAIL 2\n",
                            "kernel BUG at net/core/dev.c:2648!\n",
                        ],
                    },
                    "status": {
                        "type": "string",
                        "description":
                            "The test status string, one of the following. "
                            "\"FAIL\" - the test has failed, the tested code "
                            "is faulty. "
                            "\"ERROR\" - the test is faulty, "
                            "the status of the tested code is unknown. "
                            "\"PASS\" - the test has passed, the tested code"
                            " is correct. "
                            "\"DONE\" - the test has finished successfully, "
                            "the status of the tested code is unknown. "
                            "\"SKIP\" - the test wasn't executed, "
                            "the status of the tested code is unknown.\n"
                            "\n"
                            "The status names above are listed in priority"
                            " order (highest to lowest), which could be used"
                            " for producing a summary status for a collection"
                            " of test runs, e.g. for all testing done on "
                            "a build, based on results of executed test "
                            "suites. The summary status would be the "
                            "highest priority status across all test "
                            "runs in a collection.",
                        "enum": ["FAIL", "ERROR", "PASS", "DONE", "SKIP"],
                    },
                    "waived": {
                        "type": "boolean",
                        "description":
                            "True if the test status should be ignored.\n"
                            "\n"
                            "Could be used for reporting test results without "
                            "affecting the overall test status and alerting "
                            "the contacts concerned with the checked out and "
                            "tested source code. For example, for collecting "
                            "test reliability statistics when the test is "
                            "first introduced, or is being fixed.",
                    },
                    "start_time": {
                        "type": "string",
                        "format": "date-time",
                        "description":
                            "The time the test run was started",
                        "examples": [
                            "2020-08-14T23:08:06.967000+00:00",
                        ],
                    },
                    "duration": {
                        "type": "number",
                        "description":
                            "The number of seconds it took to run the test",
                    },
                    "output_files": {
                        "description":
                            "A list of test outputs: logs, dumps, etc. "
                            "Except the file referenced by \"log_url\".",
                        "$ref": "#/$defs/resource_list"
                    },
                    "misc": {
                        "type": "object",
                        "description":
                            "Miscellaneous extra data about the test run",
                    },
                },
                "additionalProperties": False,
                "required": ["build_id", "id", "origin"],
            },
        },

        "properties": {
            "version": {
                "type": "object",
                "properties": {
                    "major": {
                        "type": "integer",
                        "const": major,
                        "description":
                            "Major number of the schema version.\n"
                            "\n"
                            "Increases represent backward-incompatible "
                            "changes. E.g. deleting or renaming a "
                            "property, changing a property type, "
                            "restricting values, making a property "
                            "required, or adding a new required "
                            "property.",
                    },
                    "minor": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": minor,
                        "description":
                            "Minor number of the schema version.\n"
                            "\n"
                            "Increases represent backward-compatible "
                            "changes. E.g. relaxing value restrictions, "
                            "making a property optional, or adding a new "
                            "optional property.",
                    }
                },
                "additionalProperties": False,
                "required": [
                    "major",
                ],
            },
            "checkouts": {
                "description": "List of source code checkouts",
                "type": "array",
                "items": {"$ref": "#/$defs/checkout"},
            },
            "builds": {
                "description": "List of builds",
                "type": "array",
                "items": {"$ref": "#/$defs/build"},
            },
            "tests": {
                "description": "List of test runs",
                "type": "array",
                "items": {"$ref": "#/$defs/test"},
            },
        },
        "additionalProperties": False,
        "required": [
            "version",
        ],
    }

    # The parent-child relationship tree
    tree = {
        "": ["checkouts"],
        "checkouts": ["builds"],
        "builds": ["tests"],
        "tests": []
    }

    @classmethod
    def _inherit(cls, data):
        """
        Inherit data, i.e. convert data adhering to the previous version of
        the schema to satisfy this version of the schema.

        Args:
            data:   The data to inherit. Will be modified in place.

        Returns:
            The inherited data.
        """
        # Inherit revisions
        if 'revisions' in data:
            for revision in data['revisions']:
                # Generate checkout ID from the origin and revision ID.
                # Assume everyone sending older schema versions only uses their
                # own revisions, and prevent losing most data to deduplication.
                # Use placeholder origin to avoid clashes with actual
                # checkouts.
                revision['id'] = \
                    '_:' + revision['origin'] + ':' + revision['id']
                # Rename "patch_mboxes" to "patchset_files"
                if 'patch_mboxes' in revision:
                    revision['patchset_files'] = revision.pop('patch_mboxes')
                # Extract patchset hash, if any
                try:
                    revision['patchset_hash'] = revision['id'].split("+")[1]
                except IndexError:
                    revision['patchset_hash'] = ""
                # Rename "discovery_time" to "start_time"
                if 'discovery_time' in revision:
                    revision['start_time'] = revision.pop('discovery_time')
                # Rename 'description' to 'comment'
                if 'description' in revision:
                    revision['comment'] = revision.pop('description')
                # Remove "publishing_time"
                revision.pop('publishing_time', None)
            # Rename "revisions" to "checkouts"
            data['checkouts'] = data.pop('revisions')

        # Inherit builds
        for build in data.get('builds', []):
            # Generate checkout ID from the origin and revision ID.
            # Assume everyone sending older schema versions only uses their
            # own revisions, and prevent losing most data to deduplication.
            # Use placeholder origin to avoid clashes with actual checkouts.
            build['checkout_id'] = '_:' + build['origin'] + ':' + \
                build.pop('revision_id')
            # Rename 'description' to 'comment'
            if 'description' in build:
                build['comment'] = build.pop('description')

        # Inherit tests
        for test in data.get('tests', []):
            # Rename 'description' to 'comment'
            if 'description' in test:
                test['comment'] = test.pop('description')
            # Inherit environment
            if 'environment' in test:
                environment = test['environment']
                # Rename 'description' to 'comment'
                if 'description' in environment:
                    environment['comment'] = environment.pop('description')

        # Update version
        data['version'] = dict(major=Version.major,
                               minor=Version.minor)
        return data
