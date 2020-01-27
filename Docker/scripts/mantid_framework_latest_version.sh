#!/usr/bin/env bash

echo $(conda search -c mantid/label/nightly -c mantid mantid | tail -1 | awk '{print substr($2, 0, 4)}')
