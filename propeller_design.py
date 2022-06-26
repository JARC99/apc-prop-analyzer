# %% Preamble

# Plotting parameters
import seaborn as sns
import matplotlib.pylab as plt
import numpy as np
import os
from scipy import interpolate
from pint import UnitRegistry
from tabulate import tabulate
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
manouver_list = ["T-O", "Climb", "Cruise"]
V_op_list = [8, 12, 17]
n_op = 8000/60
P_op = 1000*0.975
rho_op = 1.02114

# Declare the propeller family
# prop_list = ["15x4E", "15x6E", "15x7E", "15x8E", "15x10E"]
diameter = 17
pitch_array = np.array([6, 7, 8, 10, 12])
nblades = 2
prop_type = "E"
# prop_list = ["16x4E", "16x6E", "16x7E", "16x8E", "16x10E", "16x12E"]
# prop_list = ["17x6E", "17x7E", "17x8E", "17x10E", "17x12E"]
# prop_list = ["18x8E", "18x10E", "18x12E"]
# prop_liIst = ["19x8E", "19x10E", "19x12E"]
# prop_list = ["20x8E", "20x10E", "20x11E", "20x13E", "20x15E"]


# %% Computations and plotting

fig, axes = plt.subplots(2, sharex=True, dpi=DPI, facecolor=FACECOLOR)
ax1 = axes[0]
ax2 = axes[1]
ax1.set_ylabel(r'$\mathdefault{\eta_{p}}$')
ax2.set_xlabel(r'$\mathdefault{C_{S}}$')
ax2.set_ylabel('J')

J_func_list = []
eta_p_func_list = []
CT_func_list = []
CP_func_list = []
for k, pitch in enumerate(pitch_array):
    prop_name = "D{0}P{1}B{2}T{3}".format(
        diameter, pitch, nblades, prop_type)

    data_file = os.path.join(AVEPERF_DATA_DIR, prop_name + ".dat")

    J_array, eta_p_array, CT_array, CP_array = np.loadtxt(
        data_file, delimiter=',', unpack=True)

    CS_array = (J_array**5/CP_array)**(1/5)

    J_from_CS = interpolate.interp1d(
        CS_array, J_array, fill_value="extrapolate")
    J_func_list.append(J_from_CS)

    eta_p_from_CS = interpolate.interp1d(
        CS_array, eta_p_array, fill_value="extrapolate")
    eta_p_func_list.append(eta_p_from_CS)

    CT_from_CS = interpolate.interp1d(
        CS_array, CT_array, fill_value="extrapolate")
    CT_func_list.append(CT_from_CS)

    CP_from_CS = interpolate.interp1d(
        CS_array, CP_array, fill_value="extrapolate")
    CP_func_list.append(CP_from_CS)

    ax1.plot(CS_array, eta_p_array, label=pitch)
    ax2.plot(CS_array, J_array)

# %% Compute maximum efficiency line

eta_p_max4CS = []
max4CS_index_list = []
J_max4CS = []
pitch_max4CS = []

CT_max4CS = []
CP_max4CS = []
for CS in CS_array:
    eta_p_list = []
    for eta_p_func in eta_p_func_list:
        eta_p = eta_p_func(CS)
        eta_p_list.append(eta_p)
    eta_p_max = max(eta_p_list)
    eta_p_max_index = eta_p_list.index(eta_p_max)

    eta_p_max4CS.append(eta_p_max)
    max4CS_index_list.append(eta_p_max_index)

    J_max4CS.append(J_func_list[eta_p_max_index](CS))
    pitch_max4CS.append(pitch_array[eta_p_max_index])

    CT_max4CS.append(CT_func_list[eta_p_max_index](CS))
    CP_max4CS.append(CP_func_list[eta_p_max_index](CS))

unq_index_list = sorted(max4CS_index_list.index(unq_index)
                        for unq_index in set(max4CS_index_list))

CS4eta_p_max_array = CS_array[unq_index_list]
eta_p_max_array = np.array(eta_p_max4CS)[unq_index_list]

J_best_array = np.array(J_max4CS)[unq_index_list]
pitch_best_array = np.array(pitch_max4CS)[unq_index_list]

CT_best_array = np.array(CT_max4CS)[unq_index_list]
CP_best_array = np.array(CP_max4CS)[unq_index_list]

eta_p_max_from_CS = interpolate.interp1d(
    CS4eta_p_max_array, eta_p_max_array, fill_value="extrapolate")

J_from_eta_p_max = interpolate.interp1d(
    eta_p_max_array, J_best_array, fill_value="extrapolate")
pitch_from_eta_p_max = interpolate.interp1d(
    eta_p_max_array, pitch_best_array, fill_value="extrapolate")

CT_from_eta_p_max = interpolate.interp1d(
    eta_p_max_array, CT_best_array, fill_value="extrapolate")
CP_from_eta_p_max = interpolate.interp1d(
    eta_p_max_array, CP_best_array, fill_value="extrapolate")

# %%

prop_best_list = []
for i, V_op in enumerate(V_op_list):
    CS_op = V_op*(rho_op/(P_op*n_op**2))**(1/5)

    eta_p_best = eta_p_max_from_CS(CS_op)
    pitch_best = pitch_from_eta_p_max(eta_p_best)
    J_best = J_from_eta_p_max(eta_p_best)

    # eta_p_list = []
    # for m, eta_p_func in enumerate(eta_p_func_list):
    #     eta_p = eta_p_func(CS_op)
    #     eta_p_list.append(eta_p)

    # eta_p_best = max(eta_p_list)
    # best_index = eta_p_list.index(eta_p_best)

    # pitch_best = prop_list[best_index][3:]
    # J_best = J_func_list[best_index](CS_op)

    ureg = UnitRegistry()
    D_convfact = (1 * ureg.meter).to(ureg.inch).magnitude
    D_best = V_op/(n_op*J_best)
    D_in = round(D_best * D_convfact, 1)

    CT_best = CT_from_eta_p_max(eta_p_max)
    T_best = round(CT_best*rho_op*n_op**2*D_best**4, 3)

    CP_best = CP_from_eta_p_max(eta_p_max)
    P_best = round(CP_best*rho_op*n_op**3*D_best**5, 3)

    prop_best = [manouver_list[i], D_in, pitch_best, round(eta_p_best*100, 2),
                  T_best, P_best]
    prop_best_list.append(prop_best)


# %% Output

# ax1.axhline(y=eta_p_best, color="black", linestyle="dotted")
# ax1.plot(CS_op, eta_p_best, marker=MARKERS[i], color="black")

# ax2.axhline(y=J_best, color="black", linestyle="dotted")
# ax2.plot(CS_op, J_best, linestyle="",
#          marker=MARKERS[i], color="black", label=manouver_list[i])

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

for ax in axes:
    # ax.axvline(x=CS_op, color="black", linestyle="dotted")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

fig.savefig(GRAPHICS_DIR + "/plot.png",
            format="png", bbox_inches="tight")

table = tabulate(prop_best_list,
                 headers=["Manouver", "Diameter, in", "Pitch, in",
                          "Propulsive Efficiency, %", "Thrust, N", "Power, W"],
                 tablefmt="pretty")
print(table)
