# Copyright (c) 2010, Fresno Pacific University
# Licensed under the New BSD license; see the LICENSE file for details.

# Remove all .pyc files in the src and test directory
find ./src -name *.pyc | xargs rm
find ./test -name *.pyc | xargs rm

# Remove the .coverage file
rm .coverage
