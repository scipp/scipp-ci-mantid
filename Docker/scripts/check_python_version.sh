#!/usr/bin/env bash

script_dir=$(realpath $(dirname "$0"))
local_py=$(python "$script_dir/local_py_version.py")

needed_py=$(bash "$script_dir/common_scipp_mantid_py_version.sh")

if [[ "$local_py" = "$needed_py" ]]; then
    echo "Python version $local_py is up to date with scipp and mantid."
    exit 0
else
    echo "Update python version to $needed_py, current version is $local_py, to be consistent with scipp and mantid"
    exit 1
fi

