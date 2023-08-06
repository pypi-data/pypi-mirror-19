#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import date

import weightanalyser.cli as cli
import weightanalyser.datahandeling as datahandeling
import weightanalyser.visualisation as visualisation


def run():
    path = os.path.expanduser("~") + "/Dropbox/weightanalyser/data/dataset.js"
    print "Hello, this is the WeightAnalyser!"
    date_format = "%d-%m-%Y"

    do_add = "y"
    while do_add == "y":
        do_add = raw_input("Do you want to add a new measurement? [y/n] ")
        if do_add == "y":
            before_today = raw_input("Is the measurement taken before today? [y/n] ")
            if before_today == "y":
                date_str = raw_input("Please enter the date you took the measurement (dd-mm-yyyy)! ")
            else:
                date_object = date.today()
                date_str = date_object.strftime(date_format)

            print date_str
            weight = float(raw_input("Enter full weight in kg! "))
            fat_perc = float(raw_input("Enter fat perc! "))
            mus_perc = float(raw_input("Enter mus perc! "))

            measurement = { "date" : date_str,
                            "weight" : float(weight),
                            "fat_perc" : float(fat_perc),
                            "fat_mass" : float(weight * fat_perc / 100.0),
                            "mus_perc" : float(mus_perc),
                            "mus_mass" : float(weight * mus_perc / 100.0) }

            dataset = cli.add_measurement(measurement)
        else:
            dataset = datahandeling.read_dataset(path)

    visualisation.make_plot(dataset)


if __name__ == "__main__":
    run()

