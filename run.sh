#!/bin/bash
cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
python3 -m venv env
source env/bin/activate
python3 -m pip install -r ./requirements.txt
python3 -m bot
