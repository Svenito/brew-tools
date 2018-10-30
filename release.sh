#!/bin/bash

# Validate tag
echo "Checking version tag"
if [[ `git describe --abbrev=0 --tags` == $1 ]]
then
    echo "Found tag"
else
    echo "Latest tag does not match version."
    exit 1
fi

# run linter
echo "Running linter....."
flake8 src --ignore=E501,W504,W503
rc=$?
if [[ $rc != 0 ]]; then
    echo "Linter Error"
    exit $rc
else
    echo "Linter OK"
fi

# run tests
echo "Running tests......"
pytest tests
rc=$?
if [[ $rc != 0 ]]; then
    echo "Tests failed"
    exit $rc
else
    echo "Tests Passed"
fi

# run build
echo "Building dist......"
python3 ./setup.py build
echo "Build OK"
exit

# upload with twine
echo "Uploading package.."
twine upload dist/*  --verbose
echo "Upload OK"