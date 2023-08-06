#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re

import weightanalyser.datahandeling as datahandeling


def add_measurement(measurement):
    """docstring for add_measurement"""
    path = os.path.expanduser("~") + "/Dropbox/weightanalyser/data/dataset.js"
    if os.path.isfile(path):
        dataset = datahandeling.read_dataset(path)
        dataset["datapoints"].append(measurement)
    else:
        dataset = {
                    "general": {"start_date": measurement["date"]},
                    "datapoints": [measurement]}
    datahandeling.write_dataset(path, dataset)

    return dataset


def check_date_format(date_string):
    if re.search('[a-zA-Z]', date_string):
        return "Contains letter!"
    if not re.search("..-..-....", date_string):
        return False
    else:
        return True
