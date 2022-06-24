"""Reformat the propeller performance files from APC Propellers."""
import os
import numpy as np
from pint import UnitRegistry

APC_DATA_DIR = "apc_data/performance"
PERF_DATA_DIR = "reformatted_data/performance"
AVEPERF_DATA_DIR = "reformatted_data/ave_performance"

# Calculate unit conversion factors.
ureg = UnitRegistry()
V_convfact = (1 * ureg.mile_per_hour).to(ureg.meter_per_second).magnitude
P_convfact = (1 * ureg.horsepower).to(ureg.watt).magnitude
Q_convfact = (1 * ureg.force_pound *
              ureg.inch).to(ureg.newton * ureg.meter).magnitude
T_convfact = (1 * ureg.force_pound).to(ureg.newton).magnitude

# Parse and reformat APC performance data files
file_list = os.listdir(APC_DATA_DIR)
for file in file_list:

    prop_name = file[5:-4]
    prop_folder = os.path.join(PERF_DATA_DIR, prop_name)
    if not os.path.exists(prop_folder):
        os.makedirs(prop_folder)

    with open(os.path.join(APC_DATA_DIR, file)) as apc_perf_file:
        line_list = apc_perf_file.readlines()

    index_list = []
    rpm_list = []
    for i, line in enumerate(line_list):
        if "PROP RPM =" in line:
            index_list.append(i)
            rpm_list.append(int(line.replace(" ", "")[8:]))

    for j, rpm in enumerate(rpm_list):

        rpm_fname = "{0}.dat".format(rpm)
        rpm_fdir = os.path.join(prop_folder, rpm_fname)
        with open(rpm_fdir, 'w') as rpm_file:
            try:
                for line in line_list[index_list[j]+4:index_list[j+1]-3]:
                    if "-NaN" not in line:
                        rpm_file.write(line)
                    else:
                        nan_index = line.find("-NaN")
                        new_line = line[:nan_index] + \
                            "     " + line[nan_index:]
                        rpm_file.write(new_line)
            except IndexError:
                for line in line_list[index_list[j]+4:]:
                    if "-NaN" not in line:
                        rpm_file.write(line)
                    else:
                        nan_index = line.find("-NaN")
                        new_line = line[:nan_index] + \
                            "     " + line[nan_index:]
                        rpm_file.write(new_line)

        rpm_file_array = np.loadtxt(rpm_fdir)
        rpm_file_array[:, 0] = rpm_file_array[:, 0]*V_convfact
        rpm_file_array[:, 5] = rpm_file_array[:, 5]*P_convfact
        rpm_file_array[:, 6] = rpm_file_array[:, 6]*Q_convfact
        rpm_file_array[:, 7] = rpm_file_array[:, 7]*T_convfact

        for k, row_array in enumerate(rpm_file_array):
            if np.any(np.isnan(row_array)):

                x = row_array[1]
                x_1 = rpm_file_array[k-1, 1]
                x_2 = rpm_file_array[k-2, 1]

                y_1 = rpm_file_array[k-1, 2:]
                y_2 = rpm_file_array[k-2, 2:]

                rpm_file_array[k, 2:] = y_1 + \
                    (x - x_1) * (y_2 - y_1)/(x_2 - x_1)

        np.savetxt(rpm_fdir, rpm_file_array[:, :8], fmt=[
            "%.1f", "%.2f", "%.4f", "%.4f", "%.4f", "%.3f", "%.3f", "%.3f"],
            header="V, J, eta_p, CT, CP, P, Q, T", delimiter=',')


# %% Create average performance files

        rpm_file_list = os.listdir(prop_folder)
        for i, rpm_file in enumerate(rpm_file_list):
            data_array = np.loadtxt(os.path.join(
                prop_folder, rpm_file), delimiter=",")
            if i == 0:
                J_array = data_array[:, 1]
                eta_p_array = data_array[:, 2]
                CT_array = data_array[:, 3]
                CP_array = data_array[:, 4]

            else:
                J_array = np.vstack((J_array, data_array[:, 1]))
                eta_p_array = np.vstack((eta_p_array, data_array[:, 2]))
                CT_array = np.vstack((CT_array, data_array[:, 3]))
                CP_array = np.vstack((CP_array, data_array[:, 4]))

        J_array = np.mean(J_array, 0)
        eta_p_array = np.mean(eta_p_array, 0)
        CT_array = np.mean(CT_array, 0)
        CP_array = np.mean(CP_array, 0)

        ave_data_array = np.vstack(
            (J_array, eta_p_array, CT_array, CP_array)).T

        np.savetxt(os.path.join(AVEPERF_DATA_DIR, prop_name + ".dat"),
                   ave_data_array, fmt=["%.1f", "%.2f", "%.4f", "%.4f"],
                   header="J, eta_p, CT, CP", delimiter=',')
