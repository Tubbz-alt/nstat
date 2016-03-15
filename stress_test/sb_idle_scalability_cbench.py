# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

""" Idle Southbound Performance test """

import cbench_utils
import common
import conf_collections_util
import controller_utils
import itertools
import logging
import multiprocessing
import os
import report_spec
import sys
import time
import util.file_ops


def sb_idle_scalability_cbench_run(out_json, ctrl_base_dir, sb_gen_base_dir,
                                   conf, output_dir):
    """Run test. This is the main function that is called from
    nstat_orchestrator and performs the specific test.

    :param out_json: the JSON output file
    :param ctrl_base_dir: controller base directory
    :param sb_gen_base_dir: cbench base directory
    :param conf: JSON configuration dictionary
    :param output_dir: directory to store output files
    :type out_json: str
    :type ctrl_base_dir: str
    :type sb_gen_base_dir: str
    :type conf: str
    :type output_dir: str
    """

    test_type = '[sb_idle_scalability_cbench]'
    logging.info('{0} initializing test parameters'.format(test_type))

    # Global variables read-write shared between monitor-main thread.
    cpid = 0
    global_sample_id = 0

    cbench_threads = multiprocessing.Value('i', 0)
    cbench_switches_per_thread = multiprocessing.Value('i', 0)
    cbench_thread_creation_delay_ms = multiprocessing.Value('i', 0)
    cbench_switches = multiprocessing.Value('i', 0)
    cbench_delay_before_traffic_ms = multiprocessing.Value('i', 0)
    cbench_simulated_hosts = multiprocessing.Value('i', 0)

    t_start = multiprocessing.Value('d', 0.0)

    # Cbench parameters
    cbench_rebuild = conf['cbench_rebuild']
    cbench_cleanup = conf['cbench_cleanup']
    cbench_name = conf['cbench_name']
    if 'mtcbench_cpu_shares' in conf:
        mtcbench_cpu_shares = conf['mtcbench_cpu_shares']
    else:
        mtcbench_cpu_shares = 100

    cbench_mode = conf['cbench_mode']
    cbench_warmup = conf['cbench_warmup']
    cbench_ms_per_test = conf['cbench_ms_per_test']
    cbench_internal_repeats = conf['cbench_internal_repeats']

    # Controller parameters
    controller_logs_dir = ctrl_base_dir + conf['controller_logs_dir']
    controller_rebuild = conf['controller_rebuild']
    controller_cleanup = conf['controller_cleanup']
    if 'controller_cpu_shares' in conf:
        controller_cpu_shares = conf['controller_cpu_shares']
    else:
        controller_cpu_shares = 100

    controller_statistics_period_ms = multiprocessing.Value('i', 0)
    # Various test parameters

    java_opts = conf['java_opts']

    # Various test parameters
    controller_node = conf_collections_util.node_parameters('Controller',
                                      conf['controller_node_ip'],
                                      int(conf['controller_node_ssh_port']),
                                      conf['controller_node_username'],
                                      conf['controller_node_password'])
    cbench_node = conf_collections_util.node_parameters('MT-Cbench', conf['cbench_node_ip'],
                                   int(conf['cbench_node_ssh_port']),
                                   conf['cbench_node_username'],
                                   conf['cbench_node_password'])
    controller_handlers_set = conf_collections_util.controller_handlers(
        ctrl_base_dir + conf['controller_build_handler'],
        ctrl_base_dir + conf['controller_start_handler'],
        ctrl_base_dir + conf['controller_status_handler'],
        ctrl_base_dir + conf['controller_stop_handler'],
        ctrl_base_dir + conf['controller_clean_handler'],
        ctrl_base_dir + conf['controller_statistics_handler'],
        ''
        )
    cbench_handlers_set = conf_collections_util.cbench_handlers(
        sb_gen_base_dir + conf['cbench_build_handler'],
        sb_gen_base_dir + conf['cbench_clean_handler'],
        sb_gen_base_dir + conf['cbench_run_handler'])
    controller_sb_interface = conf_collections_util.controller_southbound(
        conf['controller_node_ip'], conf['controller_port'])
    controller_nb_interface = conf_collections_util.controller_northbound(
        conf['controller_node_ip'], conf['controller_restconf_port'],
        conf['controller_restconf_user'], conf['controller_restconf_password'])
    # list of samples: each sample is a dictionary that contains all
    # information that describes a single measurement, i.e.:
    #    - the actual performance results
    #    - secondary runtime statistics
    #    - current values of test dimensions (dynamic)
    #    - test configuration options (static)
    total_samples = []

    try:
        # Before proceeding with the experiments check validity of all
        # handlers
        logging.info('{0} checking handler files.'.format(test_type))
        util.file_ops.check_filelist([
            controller_handlers_set.ctrl_build_handler,
            controller_handlers_set.ctrl_start_handler,
            controller_handlers_set.ctrl_status_handler,
            controller_handlers_set.ctrl_stop_handler,
            controller_handlers_set.ctrl_clean_handler,
            controller_handlers_set.ctrl_statistics_handler,
            cbench_handlers_set.cbench_build_handler,
            cbench_handlers_set.cbench_run_handler,
            cbench_handlers_set.cbench_clean_handler])

        # Opening connection with cbench node and returning
        # cbench_ssh_client to be utilized in the sequel
        cbench_ssh_client, controller_ssh_client, = \
            common.open_ssh_connections([cbench_node, controller_node])

        controller_cpus, cbench_cpus = common.create_cpu_shares(
            controller_cpu_shares, mtcbench_cpu_shares)

        if cbench_rebuild:
            logging.info('{0} building cbench.'.format(test_type))
            cbench_utils.rebuild_cbench(
                cbench_handlers_set.cbench_build_handler, cbench_ssh_client)

        # Controller common pre actions:
        # 1. rebuild controller if controller_rebuild is SET
        # 2. check_for_active controller,
        # 3. generate_controller_xml_files
        controller_utils.controller_pre_actions(controller_handlers_set,
                                      controller_rebuild, controller_ssh_client,
                                      java_opts, controller_sb_interface.port,
                                      controller_cpus)

        # Run tests for all possible dimensions
        for (cbench_threads.value,
             cbench_switches_per_thread.value,
             cbench_thread_creation_delay_ms.value,
             cbench_delay_before_traffic_ms.value,
             cbench_simulated_hosts.value,
             controller_statistics_period_ms.value) in \
             itertools.product(conf['cbench_threads'],
                               conf['cbench_switches_per_thread'],
                               conf['cbench_thread_creation_delay_ms'],
                               conf['cbench_delay_before_traffic_ms'],
                               conf['cbench_simulated_hosts'],
                               conf['controller_statistics_period_ms']):

            print(controller_statistics_period_ms.value)
            logging.info('{0} changing controller statistics period to {1} ms'.
                format(test_type, controller_statistics_period_ms.value))
            controller_utils.controller_changestatsperiod(
                controller_handlers_set.ctrl_statistics_handler,
                controller_statistics_period_ms.value, controller_ssh_client)

            logging.info('{0} starting controller'.format(test_type))
            cpid = controller_utils.start_controller( controller_handlers_set,
                controller_sb_interface.port, ' '.join(conf['java_opts']),
                controller_cpus, controller_ssh_client)
            logging.info('{0} OK, controller status is 1.'.format(test_type))

            cbench_switches.value = \
                cbench_threads.value * cbench_switches_per_thread.value

            logging.info('{0} creating queue'.format(test_type))
            result_queue = multiprocessing.Queue()

            topology_start_time_ms = \
                cbench_threads.value * cbench_thread_creation_delay_ms.value
            t_start.value = time.time()

            logging.info('{0} creating monitor thread'.format(test_type))
            monitor_thread = multiprocessing.Process(
                target=common.poll_ds_thread,
                args=(controller_nb_interface, t_start, topology_start_time_ms,
                      cbench_switches, result_queue))


            logging.info('{0} creating Cbench thread'.format(test_type))
            cbench_thread = multiprocessing.Process(
                target=cbench_utils.cbench_thread,
                args=(cbench_handlers_set.cbench_run_handler,
                      cbench_cpus, controller_node.ip,
                      controller_sb_interface.port, cbench_threads,
                      cbench_switches_per_thread,
                      cbench_switches, cbench_thread_creation_delay_ms,
                      cbench_delay_before_traffic_ms,
                      cbench_ms_per_test, cbench_internal_repeats,
                      cbench_simulated_hosts, cbench_warmup,
                      cbench_mode, cbench_node))

            # Parallel section
            monitor_thread.start()
            cbench_thread.start()

            res = result_queue.get(block=True)
            logging.info('{0} joining monitor thread'.format(test_type))
            monitor_thread.join()

            # After the monitor thread joins, we no longer need cbench
            # because the actual test has been completed and we have the
            # results. That is why we do not wait cbench thread to return
            # and we stop it with a termination signal.
            logging.info('{0} terminating cbench thread'.format(test_type))
            cbench_thread.terminate()
            # It is important to join() the process after terminating it in
            # order to give the background machinery time to update the status
            # of the object to reflect the termination.
            cbench_thread.join()

            # Results collection
            statistics = common.sample_stats(cpid, controller_ssh_client)
            statistics['global_sample_id'] = global_sample_id
            global_sample_id += 1
            statistics['cbench_simulated_hosts'] = \
                cbench_simulated_hosts.value
            statistics['cbench_switches'] = cbench_switches.value
            statistics['cbench_threads'] = cbench_threads.value
            statistics['cbench_switches_per_thread'] = \
                cbench_switches_per_thread.value
            statistics['cbench_thread_creation_delay_ms'] = \
                cbench_thread_creation_delay_ms.value
            statistics['controller_statistics_period_ms'] = \
                controller_statistics_period_ms.value
            statistics['cbench_delay_before_traffic_ms'] = \
                cbench_delay_before_traffic_ms.value
            statistics['controller_node_ip'] = controller_node.ip
            statistics['controller_port'] = str(controller_sb_interface.port)
            statistics['cbench_mode'] = cbench_mode
            statistics['cbench_ms_per_test'] = cbench_ms_per_test
            statistics['cbench_internal_repeats'] = \
                cbench_internal_repeats
            statistics['mtcbench_cpu_shares'] = \
                '{0}%'.format(mtcbench_cpu_shares)
            statistics['controller_cpu_shares'] = \
                '{0}%'.format(controller_cpu_shares)


            statistics['cbench_warmup'] = cbench_warmup
            statistics['bootup_time_secs'] = res[0]
            statistics['discovered_switches'] = res[1]
            total_samples.append(statistics)

            controller_utils.stop_controller(controller_handlers_set, cpid,
                                             controller_ssh_client)

    except:
        logging.error('{0} :::::::::: Exception :::::::::::'.format(test_type))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.error('{0} Exception: {1}, {2}'.
                      format(test_type, exc_type, exc_tb.tb_lineno))

        errors = str(exc_obj).rstrip().split('\n')
        for error in errors:
            logging.error('{0} {1}'.format(test_type, error))
        logging.exception('')

    finally:
        logging.info('{0} finalizing test'.format(test_type))

        logging.info('{0} creating test output directory if not present.'.
                     format(test_type))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        logging.info('{0} saving results to JSON file.'.format(test_type))
        common.generate_json_results(total_samples, out_json)

        try:
            logging.info('{0} stopping controller.'.
                         format(test_type))
            controller_utils.stop_controller(controller_handlers_set, cpid,
                controller_ssh_client)
        except:
            pass

        try:
            logging.info('{0} collecting logs'.format(test_type))
            util.netutil.copy_dir_remote_to_local(controller_node,
                controller_logs_dir, output_dir+'/log')
        except:
            logging.error('{0} {1}'.format(
                test_type, 'failed transferring controller logs dir.'))

        if controller_cleanup:
            logging.info('{0} cleaning controller.'.format(test_type))
            controller_utils.cleanup_controller(
                controller_handlers_set.ctrl_clean_handler,
                controller_ssh_client)

        if cbench_cleanup:
            logging.info('{0} cleaning cbench.'.format(test_type))
            cbench_utils.cleanup_cbench(cbench_handlers_set.cbench_clean_handler, cbench_ssh_client)

        # Closing ssh connections with controller/cbench nodes
        common.close_ssh_connections([controller_ssh_client,
                                      cbench_ssh_client])


def get_report_spec(test_type, config_json, results_json):
    """It returns all the information that is needed for the generation of the
    report for the specific test.

    :param test_type: describes the type of the specific test. This value
    defines the title of the html report.
    :param config_json: this is the filepath to the configuration json file.
    :param results_json: this is the filepath to the results json file.
    :returns: A ReportSpec object that holds all the test report information
    and is passed as input to the generate_html() function in the
    html_generation.py, that is responsible for the report generation.
    :rtype: ReportSpec object
    :type: test_type: str
    :type: config_json: str
    :type: results_json: str
    """

    report_spec_obj = report_spec.ReportSpec(config_json, results_json,
        '{0}'.format(test_type), [report_spec.TableSpec('1d',
            'Test configuration parameters (detailed)',
            [('controller_name', 'Controller name'),
             ('controller_build_handler', 'Controller build script'),
             ('controller_start_handler', 'Controller start script'),
             ('controller_stop_handler', 'Controller stop script'),
             ('controller_status_handler', 'Controller status script'),
             ('controller_clean_handler', 'Controller cleanup script'),
             ('controller_statistics_handler', 'Controller statistics script'),
             ('controller_node_ip', 'Controller IP node address'),
             ('controller_node_ssh_port', 'Controller node ssh port'),
             ('controller_node_username', 'Controller node username'),
             ('controller_node_password', 'Controller node password'),
             ('controller_port', 'Controller Southbound port'),
             ('controller_rebuild', 'Controller rebuild between test repeats'),
             ('controller_logs_dir', 'Controller log save directory'),
             ('cbench_name', 'Generator name'),
             ('cbench_node_ip', 'Cbench node IP address'),
             ('cbench_node_ssh_port', 'Cbench node ssh port'),
             ('cbench_node_username', 'Cbench node username'),
             ('cbench_node_password', 'Cbench node password'),
             ('cbench_build_handler', 'Generator build script'),
             ('cbench_run_handler', 'Generator start script'),
             ('cbench_clean_handler', 'Generator cleanup script'),
             ('cbench_simulated_hosts', 'Generator simulated hosts'),
             ('cbench_threads', 'Generator threads'),
             ('cbench_thread_creation_delay_ms',
              'Generation delay in ms between thread creation'),
             ('cbench_switches_per_thread',
              'Switches per cbench thread'),
             ('cbench_internal_repeats', 'Generator internal repeats'),
             ('cbench_ms_per_test', 'Internal repeats duration in ms'),
             ('cbench_rebuild',
              'Generator rebuild between each test repeat'),
             ('cbench_mode', 'Generator testing mode'),
             ('cbench_warmup','Generator warmup repeats'),
             ('cbench_delay_before_traffic_ms',
              'Generator delay before sending traffic in ms'),
             ('java_opts', 'JVM options')], config_json)],
        [report_spec.TableSpec('2d', 'Test results',
            [('global_sample_id', 'Sample ID'),
             ('timestamp', 'Sample timestamp (seconds)'),
             ('date', 'Sample timestamp (date)'),
             ('cbench_internal_repeats', 'Generator Internal repeats'),
             ('bootup_time_secs', 'Time to discover switches (seconds)'),
             ('discovered_switches', 'Discovered switches'),
             ('cbench_simulated_hosts', 'Generator simulated hosts'),
             ('cbench_switches', 'Generated simulated switches'),
             ('cbench_threads', 'Generator threads'),
             ('cbench_switches_per_thread',
              'Switches per cbench thread'),
             ('cbench_thread_creation_delay_ms',
              'Delay between thread creation (ms)'),
             ('cbench_delay_before_traffic_ms',
              'Delay before PacketIn transmission (ms)'),
             ('cbench_ms_per_test', 'Internal repeats interval'),
             ('cbench_warmup', 'Generator warmup repeats'),
             ('cbench_mode', 'Generator test mode'),
             ('mtcbench_cpu_shares', 'MT-Cbench CPU percentage'),
             ('controller_node_ip', 'Controller IP node address'),
             ('controller_port', 'Controller port'),
             ('controller_java_xopts', 'Java options'),
             ('one_minute_load', 'One minute load'),
             ('five_minute_load', 'five minutes load'),
             ('fifteen_minute_load', 'fifteen minutes load'),
             ('used_memory_bytes', 'System used memory (Bytes)'),
             ('total_memory_bytes', 'Total system memory'),
             ('controller_cpu_shares', 'Controller CPU percentage'),
             ('controller_cpu_system_time', 'Controller CPU system time'),
             ('controller_cpu_user_time', 'Controller CPU user time'),
             ('controller_num_threads', 'Controller threads'),
             ('controller_num_fds', 'Controller num of fds'),
             ('controller_statistics_period_ms',
              'Controller statistics period (ms)')], results_json)])

    return report_spec_obj
