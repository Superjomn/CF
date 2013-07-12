from __future__ import division
import math

def cal_entropy(ps):
    """ calculate entropy 

    ps : list of properties
        format: [...]
    """
    return sum([-p * math.log(p) for p in ps])

def cal_mutual_entropy(cps, ps):
    """
    calculate mutual entropy

    cps : conditional properties
        format: [
            (p(X=i), [cp(Y|X=i), ... ]),
            ...
        ]
    ps : properties
        format: [...]
    """
    entropy1 = cal_entropy(ps)
    ce = sum([p[0] * cal_entropy(p[1]) for p in cps])
    return entropy1 - ce
