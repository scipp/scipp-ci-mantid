#!/usr/bin/env bash

echo $(conda search -c scipp/label/dev scipp | tail -1 | awk '{print substr($3, 3, 1)"."substr($3, 4, 1)}')