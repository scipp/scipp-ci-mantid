#!/usr/bin/env bash

script_dir=$(realpath $(dirname "$0"))
scipp_py=$(bash "$script_dir/scipp_py_version.sh")
mantid_py=$(bash "$script_dir/mantid_framework_py_version.sh")

common_py=$mantid_py
if [[ "$needed_py"  > "$scipp_py" ]]; then
    common_py=$scipp_py
fi

echo $common_py
