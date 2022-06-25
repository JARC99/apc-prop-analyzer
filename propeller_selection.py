"""Plot the propeller selection diagrams."""
# %% Preamble
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import os

from scipy import interpolate
from pint import UnitRegistry
from tabulate import tabulate

# Plotting constants
DPI = 300
SUBSTACK_FLAG = True
FACECOLOR = "#f2f2e3"
COLORS = ["darkblue", "darkorange", "darkgreen", "firebrick",
          "purple", "mediumvioletred", "goldenrod", "darkcyan"]
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
V_op = 15
n_op = 8000/60
P_op = 1000
rho_op = 1.02114

CS_op = V_op*(rho_op/(P_op*n_op**2))**(1/5)

# Declare the propeller family
prop_list = ["17x6E", "17x7E", "17x8E", "17x10E", "17x12E"]


# %% Computations

fig, axes = plt.subplots(2, sharex=True, dpi=DPI)
ax1 = axes[0]
ax2 = axes[1]

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

    ax1.plot(CS_array, eta_p_array, label=prop[3:-1])
    ax2.plot(CS_array, J_array)
for ax in axes:
    if SUBSTACK_FLAG:
        for spine in ax.spines.values():
            spine.set(color="gray")
        ax.grid(visible=True, color="gray")
        ax1.legend(title="Pitch, in", facecolor=FACECOLOR, fancybox=False,
                   edgecolor="gray")
    else:
        ax1.legend(title="Pitch, in")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.axvline(x=CS_op, color="black", linestyle="dotted")

ax1.set_ylabel(r'$\mathdefault{\eta_{p}}$')
ax2.set_xlabel(r'$\mathdefault{C_{S}}$')
ax2.set_ylabel('J')

eta_p_list = []
for i, eta_p_func in enumerate(eta_p_func_list):
    eta_p = eta_p_func(CS_op)
    eta_p_list.append(eta_p)

eta_p_best = max(eta_p_list)
best_index = eta_p_list.index(eta_p_best)
ax1.axhline(y=eta_p_best, color="black", linestyle="dotted")
ax1.plot(CS_op, eta_p_best, marker='x', color="black")

pitch_best = prop_list[best_index][3:-1]
J_best = J_func_list[best_index](CS_op)
ax2.axhline(y=J_best, color="black", linestyle="dotted")
ax2.plot(CS_op, J_best, marker='x', color="black")

ureg = UnitRegistry()
D_convfact = (1 * ureg.meter).to(ureg.inch).magnitude
D_best = V_op/(n_op*J_best)
D_in = round(D_best * D_convfact, 2)

CT_best = CT_func_list[best_index](CS_op)
T_best = round(CT_best*rho_op*n_op**2*D_best**4, 3)

CP_best = CP_func_list[best_index](CS_op)
P_best = round(CP_best*rho_op*n_op**3*D_best**5, 3)


# %% Output

fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", transparent=True, bbox_inches="tight")

table = tabulate([[D_in, pitch_best, round(eta_p_best*100, 2), T_best,
                   P_best]], headers=["Diameter, in", "Pitch, in",
                                      "Propulsive Efficiency, %", "Thrust, N",
                                      "Power, W"], tablefmt="pretty")
print(table)
