# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

MTOOLS_DIR=`python -c 'from distutils.sysconfig import get_python_lib; print get_python_lib()'`/MoodleTools

# Remove all .pyc files in the src and test directory
find ./src -name *.pyc | xargs rm
find ./test -name *.pyc | xargs rm

# Remove the .coverage file
rm .coverage 2>/dev/null

# Remove the generated MANIFEST file
rm MANIFEST 2>/dev/null

echo ">> cleaning up moodle-tools"
echo "   moodle-tools is squeaky clean"
echo

# Uninstall a distribution if we need to
if [ "$1" = "uninstall" ]; then
    echo ">> uninstalling moodle-tools..."
    sudo rm /usr/local/bin/mdl-server 2>/dev/null
    sudo rm -Rf $MTOOLS_DIR 2>/dev/null
    echo "   the moodle-tools python library has been removed"
    echo
fi

# Check to see if we have any of the moodle-tools scripts in our local bin
echo ">> checking for moodle scripts ..."
if [ ls /usr/local/bin/mdl* 2>/dev/null ]; then
    :
else
    echo "   no moodle-tools scripts found"
fi
echo

# Check to see if we have the MoodleTools python package still installed
echo ">> checking for moodle-tools ..."
if [ -d "$MTOOLS_DIR" ]; then
    echo "   FOUND the moodle-tools python package"
else
    echo "   the moodle-tools python package is not installed"
fi