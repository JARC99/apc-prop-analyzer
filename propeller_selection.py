# %% Import required modules
import numpy as np

import matplotlib
matplotlib.rc('axes',edgecolor='r')
import matplotlib.pylab as plt

import seaborn as sns

import os

DPI = 300
SUBSTACK_FLAG = True
COLORS = ["darkblue", "darkorange", "darkgreen", "firebrick",
          "purple", "mediumvioletred", "dimgrey", "darkcyan"]
GRAPHICS_DIR = "graphics"

if SUBSTACK_FLAG:
    sns.set_theme(style="whitegrid", font="monospace",
              context="paper", palette=COLORS)
else:
    sns.set_theme(style="whitegrid", font="Palatino Linotype",
          context="paper", palette=COLORS)

prop_list = ["15x4E", "15x6E", "15x7E", "15x8E", "15x10E"]


fig, axes = plt.subplots(2, sharex=True, dpi=DPI)
ax1 = axes[0]
ax2 = axes[1]

for k, prop in enumerate(prop_list):

    DATA_DIR = "performance_data/" + prop + "/"
    file_list = os.listdir(DATA_DIR)

    CP_array_list = []
    J_array_list = []
    eta_p_array_list = []

    for i, file in enumerate(file_list):
        data_array = np.loadtxt(DATA_DIR + file, delimiter=",    ")
        if i == 0:
            J_array = data_array[:, 1]
            eta_p_array = data_array[:, 2]
            CP_array = data_array[:, 4]

        else:
            J_array = np.vstack((J_array, data_array[:, 1]))
            eta_p_array = np.vstack((eta_p_array, data_array[:, 2]))
            CP_array = np.vstack((CP_array, data_array[:, 4]))

    J_array = np.mean(J_array, 0).T
    eta_p_array = np.mean(eta_p_array, 0).T
    CP_array = np.mean(CP_array, 0).T

    CS_array = (J_array**5/CP_array)**(1/5)

    ax1.plot(CS_array, eta_p_array)
    ax2.plot(CS_array, J_array)

for ax in axes:
    if SUBSTACK_FLAG:
        for spine in ax.spines.values():
            spine.set(color="black", alpha=1/2)
        ax.grid(visible=True, color="black", alpha=1/2)
    else:
        pass

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

ax1.set_ylabel(r'$\mathdefault{\eta_{p}}$')
ax2.set_xlabel(r'$\mathdefault{C_{S}}$')
ax2.set_ylabel('J')


fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", transparent=True, bbox_inches="tight")

# %%
