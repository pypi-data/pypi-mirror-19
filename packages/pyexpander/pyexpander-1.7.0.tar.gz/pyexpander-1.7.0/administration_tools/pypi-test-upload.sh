#!/bin/bash

# Pypi usage taken from here:
# https://wiki.python.org/moin/TestPyPI

set -e

TOP=$(readlink -e $(dirname $0)/..)

#PYPI_SITE="https://pypi.python.org/pypi"
# Note: for test use this URL:
PYPI_SITE="https://testpypi.python.org/pypi"

if [ ! -e $HOME/.pypirc ]; then
    echo "error, $HOME/.pypirc not found"
    exit 1
fi

echo "Upload the package to Pypi"

# create documentation:
./doc-rebuild.sh

cd $TOP
python setup.py sdist upload -r $PYPI_SITE

echo "You may now view the results on"
echo "$PYPI_SITE/pyexpander"

# Note: install the package with:
# pip install pyexpander --prefix PREFIX  or
# pip install pyexpander -i $PYPI_SITE --prefix PREFIX
