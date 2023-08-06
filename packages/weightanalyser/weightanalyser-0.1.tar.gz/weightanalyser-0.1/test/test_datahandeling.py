#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# import standard libraries
import os

import weightanalyser.datahandeling as datahandeling

def test_writeread():
    """Test the wirte_datapoint and read_dataset functions of the datahandling module.

    It just writes a datapoint to a dataset in a file and reads the dataset afterwards.
    Because the datapoint is the only one in the dataset, the first index of the dataset
    should be equal to the datapoint.
    """
    datapoint = { "date" : "2016-09-13", "weight" : 90, "fat_perc" : 33, "mus_perc" : 33 }
    path = "test/testdata/test_writeread.dat"
    if os.path.exists(path):
            os.remove(path)
    datahandeling.write_dataset(path, datapoint)
    dataset = datahandeling.read_dataset(path)
    assert datapoint == dataset
