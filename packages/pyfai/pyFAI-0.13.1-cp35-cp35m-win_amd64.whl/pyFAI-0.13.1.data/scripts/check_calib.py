#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Azimuthal integration
#             https://github.com/kif/pyFAI
#
#    File: "$Id$"
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, print_function, with_statement, division
"""
check_calib

This is a very simple tool that checks a calibratation at the sub-pixel level

Deprecated

"""

__author__ = "Jerome Kieffer"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "28/11/2016"
__satus__ = "production"

import logging
import warnings
import sys

try:
    from pyFAI.third_party import six
except (ImportError, Exception):
    import six

logger = logging.getLogger("check_calib")

with warnings.catch_warnings():
    from pyFAI.calibration import CheckCalib
    warnings.simplefilter("ignore")
    import pylab

cc = None
if __name__ == "__main__":
    pylab.ion()
    cc = CheckCalib()
    if cc.parse():
        cc.integrate()
        cc.rebuild()
        cc.show()
        six.moves.input("enter to quit")
    else:
        sys.exit(1)
