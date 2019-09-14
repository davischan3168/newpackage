#!/usr/bin/env python3
# -*-coding:utf-8-*-
import datetime as dt
import numpy as np
def get_year_deltas(date_list, day_count=365.):
    """ Return vector of floats with day deltas in years.
    Initial value normalized to zero.
    Parameters
    ==========
    date_list : list or array
    collection of datetime objects
    day_count : float
    number of days for a year
    Results
    =======
    delta_list : array
    year fractions
    """
    
    start = date_list[0]
    delta_list = [(date - start).days / day_count for date in date_list]
    return np.array(delta_list)
