#! /bin/bash

source venv/bin/activate

for f in ./__tests__/*.py; do
    PYTHONPATH=$(pwd) python3 $f
done