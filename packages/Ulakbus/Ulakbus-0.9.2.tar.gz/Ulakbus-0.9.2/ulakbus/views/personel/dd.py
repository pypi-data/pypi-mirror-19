# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

__author__ = 'zops5'


class SetVars(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SetSum(object):
    def __init__(self):
        pass

    def summer(self):
        return self.x + self.y


class SetAndSum(SetVars, SetSum):
    def __init__(self, x, y):
        super(SetAndSum, self).__init__(x, y)
        self.sum = self.summer()

summ = SetAndSum(5, 6)

print(dir(summ))

print(summ.sum)