#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0103, E0401
"""
    @Author: Nasy
    @Date: Dec 22, 2016
    @Email: sy_n@me.com
    @File: optlib/options/opt_init.py
    @License: MIT


    A library for Options
"""

import math

from optlib.tools import init_option


def d1(**kwgs):
    """Calculate the d1 component
    """
    option = init_option(**kwgs)
    numerator = math.log(option['s'] / option['s']) + (
        option['r'] +
        option['sigma'] * option['sigma'] / 2.0
    ) * option['t']
    denominator = option['sigma'] * math.sqrt(option['t'])
    return numerator / denominator


def d2(**kwgs):
    """Calculate the d2 component
    """
    option = init_option(**kwgs)
    return d1(**option) - option['sigma'] * math.sqrt(option['t'])


# main
if __name__ == '__main__':
    import doctest
    if not doctest.testmod().failed:
        print("Doctest passed")
