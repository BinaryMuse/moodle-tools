moodle-tools
============

![moodle-tools](http://binarymuse.github.com/moodle-tools/moodle_tools.png)

What is moodle-tools
--------------------

moodle-tools is a collect of programs used to facilitate administering Moodle
installations. Configuration files store information about one or more
servers, and all moodle-tools programs use this configuration data.

Getting Help
------------

Every program included in moodle-tools shows helpful output with the `-h` or
`--help` option.

It Can Do
---------

*   `mdl-server` - Shows server configuration data as defined in an XML-based
    configuration file (by default located at `mdl-server.xml`--you can
    choose a different file by passing the `--file=FILE` option). This XML
    file allows you to define an installation directory and a data directory
    for one or more installations of Moodle on one or more servers.

    Other programs that need to access information about your Moodle
    installations will use the output from `mdl-server` to do so.

It Might Will Can Do
--------------------

*   `mdl-archive` - Archive a working git branch or a source distribution
    to a file
*   `mdl-deploy` - Deploy a working git branch, source distribution, or
    archive file to a working Moodle installation. Can use data from
    `mdl-server` to determine installation locations
*   `mdl-maintenance` - Turn maintenance mode on or off for a Moodle
    installation.
*   `mdl-backup` - Back up certain parts of a Moodle installation, including
    source code, data directory, and database schema and data.
*   `mdl-roll-course` - Back up a current course and restore it into a new
    course. (Might be easier to use RPC mechanisms?)

Dependencies
------------

moodle-tools is written in Python, so you will obviously need a working
installation. I currently work with version 2.6.1.

moodle-tools currently depends on the following:

*   xml.minidom
*   optparse
*   unittest

Contributing
------------

moodle-tools is still in very early planning and development. I decided to
put it on GitHub to get things organized and give anyone who might be crazy
enough to be interested a chance to take a look at it.

Most of these tools stem from specific needs that I have managing the
multiple Moodle installations I have to administer, so some of the tools may
feel very specific, and the package may feel pretty narrow. I'd like to
expand this into a generic toolset that works for a good number of other people.

If you'd like to contribute code, feel free to fork the project, make changes,
and initiate a pull request. It'd be nice if changes came with documentation
and unit tests, but it's not required (yet). I'm not 100% sure how I want
the documentation to work yet (HTML? man pages?), so I haven't checked anything
in quite yet. However, every program should present helpful information
via `mdl-program --help` or `mdl-program -h`.

Clone the project with `git clone git://github.com/BinaryMuse/moodle-tools.git`

Notes
-----

Notes (thoughts, discussion, etc.) for moodle-tools is held at the
[GitHub wiki for moodle-tools](http://wiki.github.com/BinaryMuse/moodle-tools/).

Running Unit Tests
------------------

If you are working off of the source distribution of moodle-tools (checked
out from git or downloaded as a source archive), your directory structure
should resemble the following:

    .gitignore
    README.md
    clean.sh
    rununittests.sh
    src/
      source files
    test/
      unit tests

To run the unit tests, be sure to have the `nose` module installed, change
directories into the root of the source distribution, and run
`./rununittests`. This runs `nosetests` with the appropriate coverage options.

Licensing
---------

Copyright (c) 2010, Fresno Pacific University

Licensed under the New BSD license; see the LICENSE file for details.
