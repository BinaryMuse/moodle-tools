# Remove all .pyc files in the src and test directory
find ./src -name *.pyc | xargs rm
find ./test -name *.pyc | xargs rm