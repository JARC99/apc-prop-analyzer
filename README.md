# apc-prop-analyzer
A set of scripts design to work with the propeller performance data published by APC propellers on their [website](https://www.apcprop.com/technical-information/performance-data/). A summary of the uses of the different scripts follows.

## apc_file_reformatter.py
This script is used to process the original propeller data into a more usable format. Besides extracting the preformance data of each test condition and saving it into an individual file and computing the average performance metrics of each propeller, the script converts all measured quantities to SI units and renames the files following the format *D(diameter)P(pitch)B(blade number)T(type)* to ease working with them in the future. The script's output is stored in the *reformatted_data* folder.

## propeller_selection.py
From a given set of options, peforms a performance-based analysis to aid in the selection of a fixed pitch propeller.

## convperf_plots.py
Plots the performance curves for a selection of propellers.
