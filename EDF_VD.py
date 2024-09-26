# CPS Replicate
# Mahdi Ghassab
# 401212443
from SchedulableStatus import SchedulableStatus
class EDF_VD:
    @staticmethod
    def schedulable(tasks, failure_req):
        compliant = EDF_VD.checkCompliance(tasks, failure_req)
        schedulable = EDF_VD.checkSchedulable(tasks, failure_req)
        
        if compliant:
            if schedulable:
                return SchedulableStatus.COMPLETE
            else:
                return SchedulableStatus.ONLY_COMPLIANT
        else:
            if schedulable:
                return SchedulableStatus.ONLY_SCHEDULABLE
            else:
                return SchedulableStatus.NONE

    @staticmethod
    def checkCompliance(tasks, failure_req):
        success_probs = [1 - task[4] for task in tasks]

        for i in range(len(tasks)):
            for j in range(len(tasks)):
                if tasks[j][3] < tasks[i][3]:
                    success_probs[j] *= (1 - tasks[i][4])

        for i in range(len(tasks)):
            success_probs[i] = 1 - ((1 - success_probs[i]) ** (tasks[i][3] + 1))

        for i in range(len(tasks)):
            if (1 - success_probs[i]) > failure_req[int(tasks[i][3])]:
                return False

        return True

    @staticmethod
    def checkSchedulable(tasks, failure_req):
        sum_util = sum([EDF_VD.util(i, i, tasks) for i in range(len(failure_req))])

        if sum_util <= 1:
            return True

        for c in range(len(failure_req)):
            sum_cond1 = sum([EDF_VD.util(i, i, tasks) for i in range(c + 1)])

            if sum_cond1 <= 1:
                numerator = sum([EDF_VD.util(i, c, tasks) for i in range(c + 1, len(failure_req))])
                denominator = sum([EDF_VD.util(i, i, tasks) for i in range(c + 1)])

                if denominator == 1:
                    denominator = 1 - 10e-15

                smaller_term = numerator / (1 - denominator)

                numerator = sum([EDF_VD.util(i, i, tasks) for i in range(c + 1, len(failure_req))])
                denominator = sum([EDF_VD.util(i, i, tasks) for i in range(c + 1)])

                if denominator == 0:
                    denominator = 10e-15

                compare_term = (1 - numerator) / denominator

                if smaller_term <= compare_term:
                    return True

        return False

    @staticmethod
    def util(lower, upper, tasks):
        return sum([task[0] * (upper + 1) for task in tasks if task[3] == lower])