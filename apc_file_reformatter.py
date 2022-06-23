import os
import numpy as np

from pint import UnitRegistry

APC_DATA_DIR = "apc_data/test"
NEW_DATA_DIR = "performance_data"

ureg = UnitRegistry()
V_convfact = (1 * ureg.mile_per_hour).to(ureg.meter_per_second).magnitude
P_convfact = (1 * ureg.horsepower).to(ureg.watt).magnitude
Q_convfact = (1 * ureg.force_pound *
              ureg.inch).to(ureg.newton * ureg.meter).magnitude
T_convfact = (1 * ureg.force_pound).to(ureg.newton).magnitude

file_list = os.listdir(APC_DATA_DIR)

for file in file_list:

    prop_name = file[5:-4]
    prop_folder = os.path.join(NEW_DATA_DIR, prop_name)
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

    for k, rpm in enumerate(rpm_list):

        rpm_fname = "{0}.dat".format(rpm)
        rpm_fdir = os.path.join(prop_folder, rpm_fname)
        with open(rpm_fdir, 'w') as rpm_file:
            try:
                for line in line_list[index_list[k]+4:index_list[k+1]-3]:
                    if "-NaN" not in line:
                        rpm_file.write(line)
                    else:
                        pass
            except IndexError:
                for line in line_list[index_list[k]+4:]:
                    if "-NaN" not in line:
                        rpm_file.write(line)
                    else:
                        pass

        rpm_file_array = np.loadtxt(rpm_fdir)

        rpm_file_array[:, 0] = rpm_file_array[:, 0]*V_convfact
        rpm_file_array[:, 5] = rpm_file_array[:, 5]*P_convfact
        rpm_file_array[:, 6] = rpm_file_array[:, 6]*Q_convfact
        rpm_file_array[:, 7] = rpm_file_array[:, 7]*T_convfact

        np.savetxt(rpm_fdir, rpm_file_array[:, :8], fmt=[
                   "%.1f", "%.2f", "%.4f", "%.4f", "%.4f", "%.3f", "%.3f", "%.3f"], header="V     J        eta_p      CT         CP         P         Q         T", delimiter=',    ')
