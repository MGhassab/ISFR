# CPS Replicate
# Mahdi Ghassab
# 401212443
from enum import Enum

class SchedulableStatus(Enum):
    NONE = 0
    ONLY_SCHEDULABLE = 1
    ONLY_COMPLIANT = 2
    COMPLETE = 3