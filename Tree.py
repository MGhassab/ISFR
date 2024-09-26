# CPS Replicate
# Mahdi Ghassab
# 401212443
import numpy as np
import math

class Tree:
    @staticmethod
    def schedulable(tasks, failure_req):
        max_depth = 100

        faulted_tasks = np.full(max_depth, -1, dtype=int)
        dropped_tasks = np.full((len(tasks), 2), [max_depth, -1], dtype=int)

        return Tree.buildTree(tasks, faulted_tasks, dropped_tasks, failure_req, 0)

    @staticmethod
    def buildTree(tasks, faulted_tasks, dropped_tasks, failure_req, depth):
        if depth == len(faulted_tasks):
            return True

        # failure probability due to faulted tasks
        faulted_prob = 1
        for faulted_task in faulted_tasks:
            if faulted_task != -1:
                faulted_prob *= tasks[faulted_task][4]
        if faulted_prob < failure_req[-1]:
            return True

        for i in range(len(tasks)):
            temp_depth = depth

            not_faulted_job = 0
            for j in range(temp_depth):
                if faulted_tasks[j] == i:
                    not_faulted_job += 1
            if (not_faulted_job > tasks[i][5]) or (dropped_tasks[i][0] <= not_faulted_job):
                continue

            faulted_tasks[temp_depth] = i
            temp_depth += 1

            if Tree.checkSchedulable(tasks, faulted_tasks, dropped_tasks, temp_depth):
                if not Tree.buildTree(tasks, faulted_tasks, dropped_tasks, failure_req, temp_depth):
                    return False
            else:
                # select compliance droppable tasks
                temp_dropped_task = dropped_tasks.copy()

                for j in range(len(tasks)):
                    not_faulted_job = 0
                    for k in range(temp_depth):
                        if faulted_tasks[k] == j:
                            not_faulted_job += 1
                    if (not_faulted_job > tasks[j][5]) or (temp_dropped_task[j][0] <= not_faulted_job):
                        continue

                    prev = temp_dropped_task[j][0]
                    prev_dep = temp_dropped_task[j][1]
                    if temp_dropped_task[j][1] == -1:
                        temp_dropped_task[j] = [int(tasks[j][5]), temp_depth]
                    else:
                        temp_dropped_task[j] = [temp_dropped_task[j][0] - 1, temp_depth]
                    if not Tree.checkCompliance(tasks, faulted_tasks, temp_dropped_task, failure_req):
                        temp_dropped_task[j][0] = prev
                        temp_dropped_task[j][1] = prev_dep
                        continue
                    j -= 1

                if not Tree.checkSchedulable(tasks, faulted_tasks, temp_dropped_task, temp_depth) or not Tree.buildTree(
                    tasks, faulted_tasks, temp_dropped_task, failure_req, temp_depth
                ):
                    return False

        return True


    @staticmethod
    def checkSchedulable(tasks, faulted_tasks, dropped_tasks, depth):
        # basic check
        total_sum = 0
        for i in range(depth + 1):
            total_sum += Tree.util(i, i, tasks, dropped_tasks, faulted_tasks, depth)
        if total_sum <= 1:
            return True

        # condition 1 and 2
        for c in range(depth + 1):
            # condition 1
            sum_c = 0
            for i in range(c+1):
                sum_c += Tree.util(i, i, tasks, dropped_tasks, faulted_tasks, depth)
            cond1 = sum_c <= 1
            if not cond1:
                continue

            # condition 2
            numerator = 0
            for i in range(c+1, depth+1):
                numerator += Tree.util(i, c, tasks, dropped_tasks, faulted_tasks, depth)

            denominator = 0
            for i in range(c+1):
                denominator += Tree.util(i, i, tasks, dropped_tasks, faulted_tasks, depth)

            if denominator == 1:
                denominator = 1 - 10e-15

            smaller_term = numerator / (1 - denominator)

            numerator = 0
            for i in range(c+1, depth+1):
                numerator += Tree.util(i, i, tasks, dropped_tasks, faulted_tasks, depth)

            denominator = 0
            for i in range(c+1):
                denominator += Tree.util(i, i, tasks, dropped_tasks, faulted_tasks, depth)

            if denominator == 0:
                denominator = 10e-15

            compare_term = (1 - numerator) / denominator

            cond2 = smaller_term <= compare_term

            if cond2:
                return True

        return False

    @staticmethod
    def checkCompliance(tasks, faulted_tasks, dropped_tasks, failure_req):
        success_probs = [0] * len(tasks)
        for i in range(len(tasks)):
            success_probs[i] = 1 - tasks[i][4]

        for i in range(len(tasks)):
            faulted_prob = 1
            for faulted_task in faulted_tasks:
                if faulted_task != i and faulted_task != -1:
                    faulted_prob *= tasks[faulted_task][4]

            if tasks[i][5] < dropped_tasks[i][0]:
                success_probs[i] = 1 - math.pow(1 - success_probs[i], tasks[i][5] + 1) * faulted_prob
            elif dropped_tasks[i][0] == 0:
                success_probs[i] = 1 - faulted_prob
            else:
                success_probs[i] = 1 - math.pow(1 - success_probs[i], dropped_tasks[i][0]) * faulted_prob

        for i in range(len(tasks)):
            if 1 - success_probs[i] > failure_req[int(tasks[i][3])]:
                return False

        return True

    @staticmethod
    def util(lower, upper, tasks, dropped_tasks, faulted_tasks, depth):
        total_sum = 0
        for i in range(len(tasks)):
            faulted_count = 0
            for faulted_task in faulted_tasks:
                if upper == faulted_count:
                    break
                if faulted_task == i:
                    faulted_count += 1

            if dropped_tasks[i][1] == -1 or dropped_tasks[i][0] != 0:
                criticality_level = depth
            else:
                criticality_level = dropped_tasks[i][1]

            if criticality_level == lower:
                if faulted_count <= tasks[i][5]:
                    total_sum += tasks[i][0] * (faulted_count + 1)
        return total_sum