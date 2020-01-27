#!/usr/bin/env bash

echo $(conda search -c mantid/label/nightly -c mantid mantid-framework | tail -1 | awk '{print substr($3, 3, 1)"."substr($3, 4, 1)}')
