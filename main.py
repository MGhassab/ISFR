# CPS Replicate
# Mahdi Ghassab
# 401212443
from TaskGenerator import TaskGenerator
from SchedulableStatus import SchedulableStatus
from EDF import EDF
from EDF_VD import EDF_VD
from Tree import Tree


import matplotlib.pyplot as plt
import numpy as np
class Main:
    def plot(experiments, cas, n_set, fault_rate, experiments_count):
        msg = {
            0: "EDF",
            1: "MC",
        }.get(cas, "Tree")

        # plot based util
        x_data = np.linspace(0.05, 1.0, 20)

        for i in range(len(fault_rate)):
            fig, axs = plt.subplots(3, 1, figsize=(6, 12))
            fig.suptitle(f"{msg} (fault rate = {fault_rate[i]})")

            for j in range(len(n_set)):
                y_data1 = np.zeros(20)
                y_data2 = np.zeros(20)
                y_data3 = np.zeros(20)

                for k in range(20):
                    index = k + j * 20 + i * 20 * len(n_set)
                    y_data1[k] = experiments[cas][index][3] / experiments_count
                    y_data2[k] = experiments[cas][index][4] / experiments_count
                    y_data3[k] = experiments[cas][index][5] / experiments_count

                axs[0].plot(x_data, y_data1, label=f"n = {n_set[j]}")
                axs[0].set_title("Schedulable")
                axs[0].set_xlabel("Utilization")
                axs[0].set_ylabel("Probability")

                axs[1].plot(x_data, y_data2, label=f"n = {n_set[j]}")
                axs[1].set_title("Compliant")
                axs[1].set_xlabel("Utilization")
                axs[1].set_ylabel("Probability")

                axs[2].plot(x_data, y_data3, label=f"n = {n_set[j]}")
                axs[2].set_title("Schedulable + Compliant")
                axs[2].set_xlabel("Utilization")
                axs[2].set_ylabel("Probability")

            plt.tight_layout()
            plt.show()


experiments_count = 100
failure_req = [1e-3, 1e-5, 1e-7, 1e-9]  # per hour
fault_rate = [1e-3, 1e-4, 1e-5]  # per hour
max_period = 1000
min_period = 50
n_set = [5, 10, 25, 50]

experiments = [[[0] * 6 for _ in range(len(n_set) * len(fault_rate) * 20)] for _ in range(3)]  # 0: fault rate, 1: n, 2: total util, 3: schedulable_count, 4: compliant_count, 5: complete

for fr in range(len(fault_rate)):
    for ni in range(len(n_set)):
        for u in range(1, 21, 1):
            schedulable_count_edf = 0
            schedulable_count_edf_vd = 0
            compliant_count_edf_vd = 0
            complete_count_edf_vd = 0
            schedulable_count_tree = 0

            for i in range(experiments_count):
                tasks = TaskGenerator.generate(n_set[ni], u / 20, failure_req, fault_rate[fr], min_period, max_period)
                if EDF.schedulable(tasks):
                    schedulable_count_edf += 1
                res_edf_vd = EDF_VD.schedulable(tasks, failure_req)
                if res_edf_vd == SchedulableStatus.COMPLETE:
                    schedulable_count_edf_vd += 1
                    compliant_count_edf_vd += 1
                    complete_count_edf_vd += 1
                elif res_edf_vd == SchedulableStatus.ONLY_SCHEDULABLE:
                    schedulable_count_edf_vd += 1
                elif res_edf_vd == SchedulableStatus.ONLY_COMPLIANT:
                    compliant_count_edf_vd += 1


                if Tree.schedulable(tasks, failure_req):
                    schedulable_count_tree += 1

            i = u - 1 + ni * 20 + fr * 20 * len(n_set)
            experiments[0][i] = [fr, ni, u, schedulable_count_edf, schedulable_count_edf, schedulable_count_edf]
            experiments[1][i] = [fr, ni, u, schedulable_count_edf_vd, compliant_count_edf_vd, complete_count_edf_vd]
            experiments[2][i] = [fr, ni, u, schedulable_count_tree, schedulable_count_tree, schedulable_count_tree]



based_λ = np.zeros((3, len(fault_rate), 3), dtype=np.int32)
for i in range(len(fault_rate)):
    for j in range(len(n_set)):
        for k in range(20):
            index = k + j * 20 + i * 20 * len(n_set)
            based_λ[0][i][0] += experiments[0][index][3]
            based_λ[0][i][1] += experiments[0][index][4]
            based_λ[0][i][2] += experiments[0][index][5]
            based_λ[1][i][0] += experiments[1][index][3]
            based_λ[1][i][1] += experiments[1][index][4]
            based_λ[1][i][2] += experiments[1][index][5]
            based_λ[2][i][0] += experiments[2][index][3]
            based_λ[2][i][1] += experiments[2][index][4]
            based_λ[2][i][2] += experiments[2][index][5]

print("---------------------------------------------------------------------------------------------")
print("%-10s %-15s %-15s %-15s %-20s" % ("Case", "fault rate", "Schedulable", "Compliant", "Schedulable + Compliant"))
print("---------------------------------------------------------------------------------------------")

total_per_λ = len(n_set) * 20 * experiments_count
for fr in range(len(fault_rate)):
    print("%-10s %-15s %-15s %-15s %-20s" % ("EDF", fault_rate[fr], based_λ[0][fr][0] / total_per_λ, based_λ[0][fr][1] / total_per_λ, based_λ[0][fr][2] / total_per_λ))

print("---------------------------------------------------------------------------------------------")

for fr in range(len(fault_rate)):
    print("%-10s %-15s %-15s %-15s %-20s" % ("MC", fault_rate[fr], based_λ[1][fr][0] / total_per_λ, based_λ[1][fr][1] / total_per_λ, based_λ[1][fr][2] / total_per_λ))

print("---------------------------------------------------------------------------------------------")

for fr in range(len(fault_rate)):
    print("%-10s %-15s %-15s %-15s %-20s" % ("TREE", fault_rate[fr], based_λ[2][fr][0] / total_per_λ, based_λ[2][fr][1] / total_per_λ, based_λ[2][fr][2] / total_per_λ))

print("---------------------------------------------------------------------------------------------")

Main.plot(experiments, 0, n_set, fault_rate, experiments_count)
Main.plot(experiments, 1, n_set, fault_rate, experiments_count)
Main.plot(experiments, 2, n_set, fault_rate, experiments_count)




