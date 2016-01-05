# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html



"""
Orchestrator for stress tests.
"""

import argparse
import html_generation
import json
import logging
import nb_active_mininet
import os
import sb_active_cbench
import sb_idle_cbench
import sb_idle_mininet
import shutil
import sys
import util.plot_json
import nstat_post_test_actions
import nstat_pre_test_actions


def main():
    """This is the main function where the main test application starts.
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--test',
                        required=True,
                        type=str,
                        dest='test_type',
                        action='store',
                        help="sb_active_scalability_mtcbench \n"
                             "sb_active_stability_mtcbench\n"
                             "sb_idle_scalability_mtcbench\n"
                             "sb_idle_scalability_mininet\n"
                             "nb_active_scalability_mininet")
    parser.add_argument('--bypass-execution',
                        dest='bypass_test',
                        action='store_true',
                        default=False,
                        help=('Bypass test execution and proceed to report '
                              'generation, based on a previous output.'))
    parser.add_argument('--ctrl-base-dir',
                        required=True,
                        type=str,
                        dest='ctrl_base_dir',
                        action='store',
                        help='Controller base directory')
    parser.add_argument('--sb-generator-base-dir',
                        required=True,
                        type=str,
                        dest='sb_gen_base_dir',
                        action='store',
                        help='MT-Cbench or Mininet generator base directory')
    parser.add_argument('--nb-generator-base-dir',
                        required=False,
                        type=str,
                        dest='nb_gen_base_dir',
                        action='store',
                        help='Northbound traffic generator base directory')
    parser.add_argument('--json-config',
                        required=True,
                        type=str,
                        dest='json_config',
                        action='store',
                        help='Test configuration file (JSON)')
    parser.add_argument('--json-output',
                        required=True,
                        type=str,
                        dest='json_output',
                        action='store',
                        help='Output JSON file')
    parser.add_argument('--html-report',
                        required=True,
                        type=str,
                        dest='html_report',
                        action='store',
                        help='Generated HTML report file')
    parser.add_argument('--log-file',
                        dest='log_file',
                        action='store',
                        help='File to keep test logs')
    parser.add_argument('--output-dir',
                        required=True,
                        type=str,
                        dest='output_dir',
                        action='store',
                        help='Output directory to store produced files')
    parser.add_argument('--logging-level',
                        type=str,
                        dest='logging_level',
                        action='store',
                        default='DEBUG',
                        help="Setting the level of the logging messages."
                             "Can have one of the following values:\n"
                             "INFO\n"
                             "DEBUG (default)\n"
                             "ERROR")

    args = parser.parse_args(args)

    # setting log level for NSTAT experiment
    nstat_pre_test_actions.nstat_test_set_log_level(args)

    # Parsing configuration options from JSON input file
    nstat_pre_test_actions.nstat_load_test_conf(args)

    # NSTAT test selector: depending on the test_type defined on the command
    # line options of NSTAT
    nstat_pre_test_actions.nstat_test_selector(args)

    #
    nstat_post_test_actions.nstat_post_test_actions(args)


if __name__ == '__main__':
    main()
