import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import os

# Plotting parameters
DPI = 300
PALETTE = ["darkblue", "firebrick", "forestgreen", "darkorange",
           "darkcyan", "rebeccapurple", "mediumvioletred"]
MARKERS = ['o', '^', 's', 'P', 'd']
LEGEND_FONTSIZE = "small"
GRAPHICS_DIR = "output"

sns.set_theme(style="whitegrid", font="Palatino Linotype",
              context="paper", palette=PALETTE)

# Data directory
AVEPERF_DATA_DIR = "reformatted_data/ave_performance"


# %% User input

# Declare the propeller family
prop_list = ["D17P6B2TE"]


# %% Computations and plotting

fig, axes = plt.subplots(3, sharex=True, dpi=DPI)
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

    ax1.legend(loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)


for ax in axes:
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


# %% Output

fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", bbox_inches="tight")
