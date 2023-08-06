#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  @Author: Nasy
  @Date: Dec 31, 2016
  @email: sy_n@me.com
  @file: test/test.py
  @license: MIT

  An Excited Python Script
"""

from optlib.option import Option


class TestOption:
    """The test
    """

    option = Option(
        k=30, s=30, t=0.25, r=0.025, sigma=0.44628710262841953, flag='p'
    )

    def test_price(self):
        """test price
        """
        price = abs(self.option.price.bsm - 2.56438903805528)
        assert price < 0.000001

    def test_greek(self):
        """test greek
        """
        delta = abs(self.option.greeks.delta - (-0.444495664))
        assert delta < 0.000001

    def test_print(self):
        """test print
        """
        print(self.option)
