#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import matplotlib.pyplot as plt

import weightanalyser.dataanalyser as dataanalyser


def make_function_dataset(slope, intersec, start_date_number, end_date_number):
    """docstring for make_function_dataset"""
    function_dataset = [[],[]]
    
    for i in range(start_date_number, end_date_number):
        function_dataset[0].append(i)
        function_dataset[1].append(i * slope + intersec)

    return function_dataset
    
def make_plot(dataset):
    """docstring for make_plot"""
    parameters = dataanalyser.calc_parameters(dataset, 14)
    dataset_start_date = dataset["general"]["start_date"]
    start_index = parameters["start_index"]
    start_date_number = dataanalyser.get_number_from_date(dataset["datapoints"][start_index]["date"], dataset_start_date)
    last_index = parameters["last_index"]
    datenumbers = []
    weights = []
    fat_masses = []
    mus_masses = []
    for i in range(len(dataset["datapoints"])):
        datenumbers.append(
                            dataanalyser.get_number_from_date(
                                dataset["datapoints"][i]["date"],
                                dataset["general"]["start_date"]))
        weights.append(dataset["datapoints"][i]["weight"])
        fat_masses.append(dataset["datapoints"][i]["fat_mass"])
        mus_masses.append(dataset["datapoints"][i]["mus_mass"])

    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    ax1.set_title("Full Mass")
    ax1.set_ylabel("full mass [kg]")
    ax1.grid()
    full_change_per_week = parameters["weights_parameters"][0] * 7
    full_change_per_day = parameters["weights_parameters"][0]
    full_intersec = parameters["weights_parameters"][1]
    textstr1 = "%.2f kg total / week" % (full_change_per_week)
    props = dict(boxstyle='round', facecolor='white')
    ax1.text(
                0.755, 0.95, textstr1, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top', bbox=props)
    ax1.plot(datenumbers, weights)
    
    weight_function_dataset = make_function_dataset(parameters["weights_parameters"][0],
                                                parameters["weights_parameters"][1],
                                                start_date_number,
                                                last_index)
    ax1.plot(weight_function_dataset[0], weight_function_dataset[1])

    ax2.plot(datenumbers, fat_masses)
    ax2.set_title("Fat Mass")
    ax2.set_ylabel("fat mass [kg]")
    ax2.grid()
    fat_change_per_week = parameters["fat_masses_parameters"][0] * 7
    textstr2 = "%.2f kg fat / week" % (fat_change_per_week)
    textstr2 += "\n= %.2f kcal / day" % (fat_change_per_week * 1000)
    props = dict(boxstyle='round', facecolor='white')
    ax2.text(
                0.755, 0.95, textstr2, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)

    fat_function_dataset = make_function_dataset(parameters["fat_masses_parameters"][0],
                                                parameters["fat_masses_parameters"][1],
                                                start_date_number,
                                                last_index)
    ax2.plot(fat_function_dataset[0], fat_function_dataset[1])


    ax3.plot(datenumbers, mus_masses)

    ax3.set_title("Muscle Mass")
    ax3.set_ylabel("muscle mass [kg]")
    ax3.grid()
    ax3.set_xlabel(
            "Days since start date (" + dataset["general"]["start_date"] + ")")
    muscle_change_per_week = parameters["mus_masses_parameters"][0] * 7
    textstr3 = "%.2f kg muscle / week" % (muscle_change_per_week)
    props = dict(boxstyle='round', facecolor='white')
    ax3.text(
                0.01, 0.95, textstr3, transform=ax3.transAxes, fontsize=10,
                verticalalignment='top', bbox=props
            )

    mus_function_dataset = make_function_dataset(parameters["mus_masses_parameters"][0],
                                                parameters["mus_masses_parameters"][1],
                                                start_date_number,
                                                last_index)
    ax3.plot(mus_function_dataset[0], mus_function_dataset[1])

    path = os.path.expanduser("~") + "/Dropbox/weightanalyser/data/plot.png"
    plt.savefig(path)
