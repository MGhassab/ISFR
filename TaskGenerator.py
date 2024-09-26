# CPS Replicate
# Mahdi Ghassab
# 401212443
import random
import math
class TaskGenerator:
    @staticmethod
    def generate(n, total_utility, failure_req, fault_rate, min_period, max_period):
        tasks = [[0] * 6 for _ in range(n)]
        random.seed()

        # UUniFast Algorithm
        sum = total_utility
        for i in range(n - 1):
            next_sum = sum * math.pow(random.random(), 1 / (n - i - 1))
            tasks[i][0] = sum - next_sum
            sum = next_sum
        tasks[n - 1][0] = sum

        # randomly generate periods of tasks (and calculate wcet)
        for i in range(n):
            tasks[i][1] = random.randint(min_period, max_period)
            tasks[i][2] = tasks[i][0] * tasks[i][1]

        # randomly select failure requirement (criticality level)
        for i in range(n):
            tasks[i][3] = random.randint(0, len(failure_req) - 1)

        # calculate failure probability per hour
        for i in range(n):
            n_act = (60 * 60 * 1000) / tasks[i][1]
            failure_prob_per_job = 1 - math.pow(1 - fault_rate, 1.0 / n_act)
            tasks[i][4] = 1 - math.pow(1 - failure_prob_per_job, 3600000 / tasks[i][1])

            if tasks[i][4] < 1e-15:
                tasks[i][4] = 0

        # calculate number of re-executions needed
        for i in range(n):
            if tasks[i][4] == 0:
                tasks[i][5] = 0
            else:
                tasks[i][5] = max(0, math.ceil(math.log10(failure_req[int(tasks[i][3])]) / math.log10(tasks[i][4])) - 1)
        return tasks