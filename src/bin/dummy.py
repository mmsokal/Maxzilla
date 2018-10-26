#!/usr/bin/env

import argparse as ap
import sys

myVersion = '1.0-1'

parser = ap.ArgumentParser(description="This is part of the monitoring of WiMax. It was developed to work as a " +
                                             "replacement for Maxzilla. \n" +
                                             "This processes the 'Tolopogy.xml'.")

parser.add_argument('-v', '--version', action='version', version='%s v%s' % (sys.argv[0], myVersion),
                    help="Display the version of this program")

parser.add_argument('nbiPath', metavar='PATH_TO_NBI', type=str,
                    help="Path to the NBI. The 'periodic/Topoloy/Topology.xml' must exist within")

group = parser.add_mutually_exclusive_group(required=True)


group.add_argument('-n', '--node-info', action='store_true', dest='nodeInfo', help="Collect and display information related to the CAPC, AP, PL, " +
                                              "SECTORS, etc...")

group.add_argument('-e', '--ems-info', action='store_true', dest='emsInfo', help="Collect and display information related to the EMS.")

args = parser.parse_args()

print(args)
