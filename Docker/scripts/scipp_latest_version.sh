#!/usr/bin/env bash

echo $(conda search -c scipp/label/dev scipp | tail -1 | awk '{print substr($2, 0, 4)}')
