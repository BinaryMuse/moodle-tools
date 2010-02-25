moodle-tools
============

What is moodle-tools
--------------------

moodle-tools is a collect of programs used to facilitate administering Moodle
installations. Configuration files store information about one or more
servers, and all moodle-tools programs use this configuration data.

Getting Help
------------

Every program included in moodle-tools shows helpful output with the `-h` or
`--help` option.

Included Programs
-----------------

*   `mdl-server`

    `mdl-server` shows server configuration data as defined in an XML-based
    configuration file (by default located at `mdl-server.xml`--you can
    choose a different file by passing the `--file=FILE` option). This XML
    file allows you to define an installation directory and a data directory
    for one or more installations of Moodle on one or more servers.

Running Unit Tests
------------------

If you are working off of the source distribution of moodle-tools (checked
out from git or downloaded as a source archive), your directory structure
should resemble the following:

    .gitignore
    clean.sh
    README
    src/
      source files
    test/
      unit tests

To run the unit tests, be sure to have the `nose` module installed, change
directories into the root of the source distribution, and run `nosetests`.
