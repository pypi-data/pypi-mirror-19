#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import sys

import logbook
import subprocrunner

import tcconfig
from .traffic_control import TrafficControl
from ._argparse_wrapper import ArgparseWrapper
from ._common import verify_network_interface
from ._error import NetworkInterfaceNotFoundError


handler = logbook.StderrHandler()
handler.push_application()


def parse_option():
    parser = ArgparseWrapper(tcconfig.VERSION)

    group = parser.parser.add_argument_group("Traffic Control")
    group.add_argument(
        "--device", required=True,
        help="network device name (e.g. eth0)")

    return parser.parser.parse_args()


def main():
    options = parse_option()
    logger = logbook.Logger("tcdel")
    logger.level = options.log_level

    subprocrunner.logger.level = options.log_level
    if options.quiet:
        subprocrunner.logger.disable()
    else:
        subprocrunner.logger.enable()

    subprocrunner.Which("tc").verify()

    try:
        verify_network_interface(options.device)
    except NetworkInterfaceNotFoundError as e:
        logger.error(e)
        return 1

    tc = TrafficControl(options.device)

    try:
        return tc.delete_tc()
    except NetworkInterfaceNotFoundError as e:
        logger.debug(e)
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
