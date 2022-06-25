# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:35:19 2022

@author: jaros
"""

"""Plot the propeller selection diagrams."""
# %% Preamble
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import os

from scipy import interpolate
from pint import UnitRegistry
from tabulate import tabulate

# Plotting parameters
DPI = 300
SUBSTACK_FLAG = True
FACECOLOR = "#f2f2e3"
COLORS = ["darkblue", "darkorange", "darkgreen", "firebrick",
          "purple", "mediumvioletred", "goldenrod", "darkcyan"]
MARKERS = ['o', '^', 's', 'P', 'd']
LEGEND_FONTSIZE = "small"
GRAPHICS_DIR = "graphics"

if SUBSTACK_FLAG:
    sns.set_theme(style="whitegrid", font="monospace",
                  context="paper", palette=COLORS)
else:
    sns.set_theme(style="whitegrid", font="Palatino Linotype",
                  context="paper", palette=COLORS)

# Data directory
AVEPERF_DATA_DIR = "reformatted_data/ave_performance"


# %% User input

# Declare the propeller family
prop_list = ["17x6E", "17x8E", "17x12E"]


# %% Computations and plotting

fig, axes = plt.subplots(3, sharex=True, dpi=DPI, facecolor=FACECOLOR)
ax1 = axes[0]
ax2 = axes[1]
ax3 = axes[2]

ax3.set_xlabel(r'J')

ax1.set_ylabel(r'$\mathdefault{C_{T}}$')
ax2.set_ylabel(r'$\mathdefault{C_{P}}$')
ax3.set_ylabel(r'$\mathdefault{\eta_{p}}$')

for k, prop in enumerate(prop_list):

    data_file = os.path.join(AVEPERF_DATA_DIR, prop + ".dat")

    J_array, eta_p_array, CT_array, CP_array = np.loadtxt(
        data_file, delimiter=',', unpack=True)
    CS_array = (J_array**5/CP_array)**(1/5)

    ax1.plot(J_array, CT_array, label=prop)
    ax2.plot(J_array, CP_array)
    ax3.plot(J_array, eta_p_array)

    if SUBSTACK_FLAG:
        for ax in axes:
            for spine in ax.spines.values():
                spine.set(color="gray")
            ax.set_facecolor(FACECOLOR)
            ax.grid(visible=True, color="gray")
        ax1.legend(title="Propeller", facecolor=FACECOLOR, fancybox=False,
                   edgecolor="gray", loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)

    else:
        ax1.legend(loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)


for ax in axes:
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)



# %% Output

fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", bbox_inches="tight")
