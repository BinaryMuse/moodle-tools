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
`--help` option. Similar to Git, you can also get help on a command by running
`mdl help COMMAND`.

It Can Do
---------

*   `mdl server` - Shows server configuration data as defined in an XML-based
    configuration file. This XML file allows you to define an installation
    directory and a data directory for one or more installations of Moodle on
    one or more servers.

    Other programs that need to access information about your Moodle
    installations will use the output from `mdl server` to do so.

    `mdl server` tries to locate a valid XML file in the following order:

    1.  Look for the file passed by the command line (`mdl server -f FILE` or
    `mdl server --file=FILE`)
    2.  Look for the file defined by the environment variable named
    `MDL_SERVER_CONFIG`
    3.  Look for a file named `mdl-server.xml` in the current working directory

    Note that if the environment variable exists and points to a valid file,
    you MUST pass `-f` or `--file` if you want to specify a different file
    (having `mdl-server.xml` in your working directory is not enough, as the
    environment variable takes precedence).

    See the file `src/mdl-server-schema.xml` for the details of how to
    construct this XML file, and `src/mdl-server.sample.xml` for a sample file.

It Might Will Can Do
--------------------

*   `mdl archive` - Archive a working git branch or a source distribution
    to a file
*   `mdl deploy` - Deploy a working git branch, source distribution, or
    archive file to a working Moodle installation. Can use data from
    `mdl server` to determine installation locations
*   `mdl maintenance` - Turn maintenance mode on or off for a Moodle
    installation.
*   `mdl backup` - Back up certain parts of a Moodle installation, including
    source code, data directory, and database schema and data.
*   `mdl roll-course` - Back up a current course and restore it into a new
    course. (Might be easier to use RPC mechanisms?)

Dependencies
------------

moodle-tools is written in Python, so you will obviously need a working
installation. Currently, any version after 2.4 will work. I personally currently
use version 2.6.1.

moodle-tools itself currently depends on no non-standard modules.

Unit tests using nose and coverage (the default in rununittests.sh) requires the
[coverage module](http://pypi.python.org/pypi/coverage)
and the [nose package](http://somethingaboutorange.com/mrl/projects/nose/).

Installation
------------

Install from the root of the repository by running `sudo python setup.py
install`. Create a source distribution by running `python setup.py sdist`.

Cleaning and/or Uninstalling
----------------------------

`clean.sh` is a bash script located at the root of the repository that helps
clean up your repository (and system, after an install).

Running `clean.sh` with no paramters removes all `.pyc` files, the `.coverage`
file created during unit testing, and the `MANIFEST` file generated by
`setup.py`.

Running `clean.sh uninstall` attempts to uninstall moodle-tools from your
system. It does this in the following way:

1.  Find out where Python keeps installed packages by looking at
    `distutils.sysconfig.get_python_lib()`.
2.  Removing `MoodleTools` from the Python library path.
3.  Removing `mdl-*` from `/usr/local/bin`. (Currently it only removes certain
    programs--at this time, just `mdl` and `mdl-server`.)

In either case, `clean.sh` runs checks to see if it can find any remnants of a
moodle-tools installation on your system. It does the following:

1.  `ls /usr/local/bin/mdl*` to try to find scripts that weren't removed.
2.  Checking for the existance of the MoodleTools folder in the Python
    library path.

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
    LICENSE
    MANIFEST.in
    README.md
    clean.sh
    rununittests.sh
    setup.py
    src/
      source files
    test/
      unit tests

To run the unit tests, be sure to have the `nose` module installed, change
directories into the root of the source distribution, and run
`./rununittests`. This runs `nosetests` with the appropriate coverage options.
If you don't have coverage installed, a simple `nosetests` will run just the
tests.

Licensing
---------

Copyright (c) 2010, Fresno Pacific University

Licensed under the New BSD license; see the LICENSE file for details.
