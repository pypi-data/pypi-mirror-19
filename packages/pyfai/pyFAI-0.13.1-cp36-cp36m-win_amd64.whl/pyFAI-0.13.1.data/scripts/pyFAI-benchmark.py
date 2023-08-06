#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Fast Azimuthal integration
#             https://github.com/kif/pyFAI
#
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Authors: Jérôme Kieffer <Jerome.Kieffer@ESRF.eu>
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
"""
pyFAI-benchmark is a small utility that runs the benchmark for azimuthal 
integration on images of various sizes
"""
__author__ = "Jérôme Kieffer, Picca Frédéric-Emmanuel"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "29/07/2016"
__status__ = "development"

try:
    from rfoo.utils import rconsole
    rconsole.spawn_server()
except ImportError:
    print("No socket opened for debugging -> please install rfoo")
try:
    from pyFAI.third_party import six
except (ImportError, Exception):
    import six

import pyFAI.benchmark

if __name__ == "__main__":
    try:
        from argparse import ArgumentParser
    except:
        from pyFAI.third_party.argparse import ArgumentParser
    description = """Benchmark for Azimuthal integration
    """
    epilog = """  """
    usage = """benchmark [options] """
    version = "pyFAI benchmark version " + pyFAI.version
    parser = ArgumentParser(usage=usage, description=description, epilog=epilog)
    parser.add_argument("-v", "--version", action='version', version=version)
    parser.add_argument("-d", "--debug",
                        action="store_true", dest="debug", default=False,
                        help="switch to verbose/debug mode")
    parser.add_argument("-c", "--cpu",
                        action="store_true", dest="opencl_cpu", default=False,
                        help="perform benchmark using OpenCL on the CPU")
    parser.add_argument("-g", "--gpu",
                        action="store_true", dest="opencl_gpu", default=False,
                        help="perform benchmark using OpenCL on the GPU")
    parser.add_argument("-a", "--acc",
                        action="store_true", dest="opencl_acc", default=False,
                        help="perform benchmark using OpenCL on the Accelerator (like XeonPhi/MIC)")
    parser.add_argument("-s", "--size", type=float,
                        dest="size", default=1000,
                        help="Limit the size of the dataset to X Mpixel images (for computer with limited memory)")
    parser.add_argument("-n", "--number",
                        dest="number", default=10, type=int,
                        help="Number of repetition of the test, by default 10")
    parser.add_argument("-2d", "--2dimention",
                        action="store_true", dest="twodim", default=False,
                        help="Benchmark also algorithm for 2D-regrouping")
    parser.add_argument("--no-1dimention",
                        action="store_false", dest="onedim", default=True,
                        help="Do not benchmark algorithms for 1D-regrouping")

    parser.add_argument("-m", "--memprof",
                        action="store_true", dest="memprof", default=False,
                        help="Perfrom memory profiling (Linux only)")
    parser.add_argument("-r", "--repeat",
                        dest="repeat", default=1, type=int,
                        help="Repeat each benchmark x times to take the best")

    options = parser.parse_args()
    if options.debug:
            pyFAI.logger.setLevel(logging.DEBUG)
    devices = ""
    if options.opencl_cpu:
        devices += "cpu,"
    if options.opencl_gpu:
        devices += "gpu,"
    if options.opencl_acc:
        devices += "acc,"
    pyFAI.benchmark.run(number=options.number, repeat=options.repeat, memprof=options.memprof, max_size=options.size,
              do_1d=options.onedim, do_2d=options.twodim, devices=devices)

    pyFAI.benchmark.pylab.ion()
    six.moves.input("Enter to quit")
