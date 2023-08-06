#!/usr/bin/env python3

"""
Lists all programs available
"""

import astrogear as ag
import argparse
import os
from collections import OrderedDict

def _get_programs_list(format):

    allinfo = OrderedDict()
    for pkgname, pkg in ag.collaborators().items():
        allinfo["Package '{}'".format(pkgname)] = ag.get_exe_info(ag.get_scripts_path(module=pkg))

    # This can be called (without much shame) a "gambiarra"
    if "pyfant" in ag.collaborators():
        import pyfant as pf
        allinfo["PFANT Fortran binaries"] = pf.get_fortrans()

    ret = format_programs(allinfo, format)

    return ret


def format_programs(allinfo, format):
    ret = []
    # will indent listing only if there is more than 1 package listed
    ind = 1 if len(allinfo) > 1 else 0
    for title, exeinfo in allinfo.items():
        ret.extend(ag.format_h1(title, format) + [""])
        linesp, module_len = ag.format_exe_info(exeinfo, format, ind)
        ret.extend(linesp)

    return ret



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=ag.SmartFormatter
    )
    parser.add_argument('format', type=str, help='Print format', nargs="?", default="text",
                        choices=["text", "markdown-list", "markdown-table"])
    args = parser.parse_args()

    print("\n".join(_get_programs_list(args.format)))

