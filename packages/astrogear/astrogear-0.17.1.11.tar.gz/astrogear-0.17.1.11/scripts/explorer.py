#!/usr/bin/env python3

"""AstroAPI Explorer --  list, visualize, and edit data files (_à la_ File Manager)"""

import astrogear as ag
import sys
import argparse
import logging


ag.logging_level = logging.INFO
ag.flag_log_file = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=ag.SmartFormatter
    )
    parser.add_argument('dir', type=str, help='directory name', default='.', nargs='?')
    args = parser.parse_args()

    app = ag.get_QApplication([])
    form = ag.XExplorer(None, args.dir)
    form.show()
    ag.place_center(form)
    sys.exit(app.exec_())
