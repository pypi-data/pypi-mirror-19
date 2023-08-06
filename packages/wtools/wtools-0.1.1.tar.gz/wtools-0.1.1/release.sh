#!/bin/bash
set -e

dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $dir

python setup.py sdist upload

version=`python -c "import wtools; print(wtools.version)"`

git tag -a v$version -m "v$version"

git push origin --tags

