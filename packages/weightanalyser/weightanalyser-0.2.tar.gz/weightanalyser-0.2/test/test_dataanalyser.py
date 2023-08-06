#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# import standard libraries

# import own libraries
import weightanalyser.dataanalyser as dataanalyser


def generate_testdataset():
    """docstring for generate_testdataset"""
    dataset = { "general" : { "start_date" : "01-09-2016" }, "datapoints" : [] }

    for i_datapoint in range(40):
        datapoint = {}
        datapoint.update( { "date" : dataanalyser.get_date_from_number(i_datapoint,
                                                                       dataset["general"]["start_date"]) })
        datapoint.update( { "weight" : 100 })
        datapoint.update( { "fat_perc" : 20 } )
        datapoint.update( { "fat_mass" : 20 } )
        datapoint.update( { "mus_perc" : 40 } )
        datapoint.update( { "mus_mass" : 40 } )

        dataset["datapoints"].append(datapoint)

    return dataset


def test_generate_testdataset():
    """docstring for test_generate_testdataset"""
    testdataset = generate_testdataset()
    assert testdataset["datapoints"][0]["date"] == "01-09-2016"
    assert testdataset["datapoints"][0]["weight"] == 100
    assert testdataset["datapoints"][0]["fat_perc"] == 20
    assert testdataset["datapoints"][0]["fat_mass"] == 20
    assert testdataset["datapoints"][0]["mus_perc"] == 40
    assert testdataset["datapoints"][0]["mus_mass"] == 40


def test_calc_parameters():
    """docstring for test_generate_testdataset"""
    testdataset = generate_testdataset()
    parameters = dataanalyser.calc_parameters(testdataset, 14)
    assert parameters["weights_parameters"][0] == 0
    assert parameters["weights_parameters"][1] == 100
    assert parameters["fat_masses_parameters"][0] == 0
    assert parameters["fat_masses_parameters"][1] == 20
    assert parameters["mus_masses_parameters"][0] == 0
    assert parameters["mus_masses_parameters"][1] == 40


def test_get_date_from_number():
    assert dataanalyser.get_date_from_number(5, "01-08-2016") == "06-08-2016"

def test_get_number_from_date():
    """docstring for test_get_number_from_date"""
    assert dataanalyser.get_number_from_date("06-08-2016", "01-08-2016") == 5


def test_get_index_of_period():
    """docstring for test_get_index_of_period"""
    dataset = generate_testdataset()
    period = 14
    assert dataanalyser.get_index_of_period(dataset, 10) == 28
