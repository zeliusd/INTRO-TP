#!/bin/bash

set -e

#python3 /api/db/pandas.py

python3 db/panda.py

exec python3 -m flask run --host=0.0.0.0 --debug
