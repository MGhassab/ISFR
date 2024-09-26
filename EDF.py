# CPS Replicate
# Mahdi Ghassab
# 401212443
class EDF:
    @staticmethod
    def schedulable(tasks):
        sum = 0
        for task in tasks:
            sum += task[0] * (task[3] + 1)
            if sum > 1:
                return False
        return True