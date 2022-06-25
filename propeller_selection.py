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

# Declare operation conditions
manouver_list = ["Cruise"]
V_op_list = [17]
n_op = 8000/60
P_op = 1000
rho_op = 1.02114

# Declare the propeller family
prop_list = ["17x6E", "17x7E", "17x8E", "17x10E", "17x12E"]


# %% Computations and plotting

fig, axes = plt.subplots(2, sharex=True, dpi=DPI, facecolor=FACECOLOR)
ax1 = axes[0]
ax2 = axes[1]
ax1.set_ylabel(r'$\mathdefault{\eta_{p}}$')
ax2.set_xlabel(r'$\mathdefault{C_{S}}$')
ax2.set_ylabel('J')

prop_best_list = []

for i, V_op in enumerate(V_op_list):
    CS_op = V_op*(rho_op/(P_op*n_op**2))**(1/5)

    J_func_list = []
    eta_p_func_list = []
    CT_func_list = []
    CP_func_list = []
    for k, prop in enumerate(prop_list):

        data_file = os.path.join(AVEPERF_DATA_DIR, prop + ".dat")

        J_array, eta_p_array, CT_array, CP_array = np.loadtxt(
            data_file, delimiter=',', unpack=True)
        CS_array = (J_array**5/CP_array)**(1/5)

        J_from_CS = interpolate.interp1d(CS_array, J_array)
        J_func_list.append(J_from_CS)

        eta_p_from_CS = interpolate.interp1d(CS_array, eta_p_array)
        eta_p_func_list.append(eta_p_from_CS)

        CT_from_CS = interpolate.interp1d(CS_array, CT_array)
        CT_func_list.append(CT_from_CS)

        CP_from_CS = interpolate.interp1d(CS_array, CP_array)
        CP_func_list.append(CP_from_CS)

        if i == 0:
            ax1.plot(CS_array, eta_p_array, label=prop[3:-1])
            ax2.plot(CS_array, J_array)

    eta_p_list = []
    for m, eta_p_func in enumerate(eta_p_func_list):
        eta_p = eta_p_func(CS_op)
        eta_p_list.append(eta_p)

    eta_p_best = max(eta_p_list)
    best_index = eta_p_list.index(eta_p_best)

    pitch_best = prop_list[best_index][3:-1]
    J_best = J_func_list[best_index](CS_op)

    ureg = UnitRegistry()
    D_convfact = (1 * ureg.meter).to(ureg.inch).magnitude
    D_best = V_op/(n_op*J_best)
    D_in = round(D_best * D_convfact, 2)

    CT_best = CT_func_list[best_index](CS_op)
    T_best = round(CT_best*rho_op*n_op**2*D_best**4, 3)

    CP_best = CP_func_list[best_index](CS_op)
    P_best = round(CP_best*rho_op*n_op**3*D_best**5, 3)

    prop_best = [manouver_list[i], D_in, pitch_best, round(eta_p_best*100, 2),
                 T_best, P_best]
    prop_best_list.append(prop_best)

    ax1.axhline(y=eta_p_best, color="black", linestyle="dotted")
    ax1.plot(CS_op, eta_p_best, marker=MARKERS[i], color="black")

    ax2.axhline(y=J_best, color="black", linestyle="dotted")
    ax2.plot(CS_op, J_best, linestyle="",
             marker=MARKERS[i], color="black", label=manouver_list[i])

    if SUBSTACK_FLAG:
        for ax in axes:
            for spine in ax.spines.values():
                spine.set(color="gray")
            ax.set_facecolor(FACECOLOR)
            ax.grid(visible=True, color="gray")
        ax1.legend(title="Pitch, in", facecolor=FACECOLOR, fancybox=False,
                   edgecolor="gray", loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)
        ax2.legend(title="Manouver", facecolor=FACECOLOR,
                   fancybox=False, edgecolor="gray", loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)
    else:
        ax1.legend(title="Pitch, in", loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)
        ax2.legend(title="Manouver", loc="upper right",
                   fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    for ax in axes:
        ax.axvline(x=CS_op, color="black", linestyle="dotted")


# %% Output

fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", bbox_inches="tight")

table = tabulate(prop_best_list,
                 headers=["Manouver", "Diameter, in", "Pitch, in",
                          "Propulsive Efficiency, %", "Thrust, N", "Power, W"],
                 tablefmt="pretty")
print(table)
