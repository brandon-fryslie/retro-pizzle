#!/bin/bash -el

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${script_dir}/../gem-sieve

python3 -m venv .venv
source .venv/bin/activate
#pip3 install -r requirements.txt

cd ${script_dir}/../gem-sieve/src

python3 -m GemSieve $@
