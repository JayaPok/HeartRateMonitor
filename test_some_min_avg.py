from heart_rate_monitoring import some_min_avg
import numpy as np
import collections


def test_some_min_avg():

    onemin_avg_log = collections.deque([1, 1, 1, 3, 3, 3])
    fivemin_avg_log = collections.deque([1, 1, 1, 3, 3, 3, 5, 5, 5, 7, 7,
                                         7, 9, 9, 9,
                                         11, 11, 11, 13, 13, 13, 15,
                                         15, 15, 17, 17, 17, 19, 19, 19])
    usermin_avg_log = collections.deque([1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9])
    usermin = 2

    a, b, c = some_min_avg(onemin_avg_log, fivemin_avg_log,
                           usermin_avg_log, usermin)
    assert a == 2
    assert b == 10
    assert c == 5
