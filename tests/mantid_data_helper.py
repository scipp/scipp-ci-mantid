# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2019 Scipp contributors (https://github.com/scipp)
# @author Dimitar Tasev

import os
import sys
from urllib import request


class MantidDataHelper:
    # Valid only for Linux. Windows is as C:\MantidExternalData
    DATA_DIR = os.path.abspath(os.path.expanduser(
        "/opt/tests/MantidExternalData"))
    DATA_LOCATION = "{data_dir}/{algorithm}/{hash}"
    DATA_FILES = {
        "CNCS_51936_event.nxs": {
            "hash": "5ba401e489260a44374b5be12b780911",
            "algorithm": "MD5"},
        "iris26176_graphite002_sqw.nxs": {
            "hash": "7ea63f9137602b7e9b604fe30f0c6ec2",
            "algorithm": "MD5"},
        "WISH00016748.raw": {
            "hash": "37ecc6f99662b57e405ed967bdc068af",
            "algorithm": "MD5"},
    }
    REMOTE_URL = "http://198.74.56.37/ftp/external-data/"\
        "{algorithm}/{hash}"

    @classmethod
    def find_file(cls, name):
        data_file = cls.DATA_FILES[name]
        data_location = cls.DATA_LOCATION.format(
            data_dir=cls.DATA_DIR,
            algorithm=data_file["algorithm"],
            hash=data_file["hash"])

        dir_name = os.path.dirname(data_location)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        if not os.path.isfile(data_location):
            query = cls.REMOTE_URL.format(algorithm=data_file["algorithm"],
                                          hash=data_file["hash"])
            data_location, http_response = request.urlretrieve(query,
                                                               data_location)

        return data_location
