# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

""" Active Southbound Performance test """

import cbench_utils
import common
import conf_collections_util
import controller_utils
import itertools
import logging
import multiprocessing
import os
import queue
import re
import report_spec
import sys
import util.file_ops
import util.netutil



def monitor(data_queue, result_queue, cpid, global_sample_id, repeat_id,
            test_repeats, cbench_switches, cbench_switches_per_thread,
            cbench_threads, cbench_delay_before_traffic_ms,
            cbench_thread_creation_delay_ms, cbench_simulated_hosts,
            cbench_ms_per_test, cbench_internal_repeats, cbench_warmup,
            cbench_mode, mtcbench_cpu_shares, controller_statistics_period_ms,
            controller_port, controller_node, controller_cpu_shares,
            term_success, term_fail):
    """ Function executed by the monitor thread

    :param data_queue: data queue where monitor receives Cbench output line
    by line
    :param result_queue: result queue used by monitor to send result to main
    :param cpid: controller PID
    :param global_sample_id: unique ascending ID for the next sample
    :param repeat_id: ID of the test repeat
    :param test_repeats: number of external iterations for a test, (i.e the
    number of times a test should be repeated to derive aggregate results)
    :param cbench_switches: total number of simulated switches
    :param cbench_switches_per_thread: number of sim. switches per thread
    :param cbench_threads: total number of Cbench threads
    :param cbench_delay_before_traffic_ms: delay before traffic transmission
    (in milliseconds)
    :param cbench_thread_creation_delay_ms: delay between thread creation
    (in milliseconds)
    :param cbench_simulated_hosts: number of simulated hosts
    :param cbench_ms_per_test: duration (in (ms)) of Cbench internal
    iteration
    :param cbench_internal_repeats: number of internal iterations during traffic
    transmission where performance and other statistics are sampled
    :param cbench_warmup: number of initial internal iterations that were
    treated as "warmup" and  are not considered when computing aggregate
    performance results
    :param cbench_mode: (one of "Latency" or "Throughput", see Cbench
    documentation)
    :param mtcbench_cpu_shares: the percentage of CPU resources to be used for
    mtcbench
    :param controller_statistics_period_ms: Interval that controller sends
    statistics flow requests to the switches (in milliseconds)
    :param controller_port: controller port number where OF switches should
    connect
    :param controller node: named tuple containing the 1) controller node IP
    address 2) ssh port of controller node (controller_node_ip) 3) username of
    the controller node 4) password of the controller node
    :param controller_cpu_shares: the percentage of CPU resources to be used for
    controller
    :param term_success: The success message when we have success in Cbench thread
    :param term_fail: The fail message
    :type data_queue: multiprocessing.Queue
    :type result_queue: multiprocessing.Queue
    :type cpid: int
    :type global_sample_id: int
    :type repeat_id: int
    :type test_repeats: int
    :type cbench_switches: int
    :type cbench_switches_per_thread: int
    :type cbench_threads: int
    :type cbench_delay_before_traffic_ms: int
    :type cbench_thread_creation_delay_ms: int
    :type cbench_simulated_hosts: int
    :type cbench_ms_per_test: int
    :type cbench_internal_repeats: int
    :type cbench_warmup: int
    :type cbench_mode: str
    :type mtcbench_cpu_shares: int
    :type controller_statistics_period_ms: int
    :type controller_port: str
    :type controller_node: namedtuple<str,str,str,str>
    :type controller_cpu_shares: int
    :type term_success: str
    :type term_fail: str
    """

    internal_repeat_id = 0
    logging.info('[monitor_thread] Monitor thread started')

    # will hold samples taken in the lifetime of this thread
    samples = []
        # Opening connection with controller node to be utilized in the sequel

    controller_ssh_client =  common.open_ssh_connections([controller_node])[0]

    while True:
        try:
            # read messages from queue while TERM_SUCCESS has not been sent
            line = data_queue.get(block=True, timeout=10000)
            #if line == term_success.value.decode():
            if line == term_success:
                logging.info('[monitor_thread] successful termination '
                              'string returned. Returning samples and exiting.')
                result_queue.put(samples, block=True)
                return
            else:
                # look for lines containing a substring like e.g.
                # 'total = 1.2345 per ms'
                match = re.search(r'total = (.+) per ms', line)
                if match is not None or line == term_fail:
                    statistics = common.sample_stats(cpid.value,
                                                     controller_ssh_client)
                    statistics['global_sample_id'] = \
                        global_sample_id.value
                    global_sample_id.value += 1
                    statistics['repeat_id'] = repeat_id.value
                    statistics['internal_repeat_id'] = internal_repeat_id
                    statistics['cbench_simulated_hosts'] = \
                        cbench_simulated_hosts.value
                    statistics['cbench_switches'] = \
                        cbench_switches.value
                    statistics['cbench_threads'] = \
                        cbench_threads.value
                    statistics['cbench_switches_per_thread'] = \
                        cbench_switches_per_thread.value
                    statistics['cbench_thread_creation_delay_ms'] = \
                        cbench_thread_creation_delay_ms.value
                    statistics['cbench_delay_before_traffic_ms'] = \
                        cbench_delay_before_traffic_ms.value
                    statistics['controller_statistics_period_ms'] = \
                        controller_statistics_period_ms.value
                    statistics['test_repeats'] = test_repeats
                    statistics['controller_node_ip'] = controller_node.ip
                    statistics['controller_port'] = str(controller_port)
                    statistics['controller_cpu_shares'] = \
                        '{0}%'.format(controller_cpu_shares)
                    statistics['cbench_mode'] = cbench_mode
                    statistics['cbench_ms_per_test'] = cbench_ms_per_test
                    statistics['cbench_internal_repeats'] = \
                        cbench_internal_repeats
                    statistics['mtcbench_cpu_shares'] = \
                        '{0}%'.format(mtcbench_cpu_shares)
                    statistics['cbench_warmup'] = cbench_warmup
                    if line == term_fail:
                        logging.info(
                            '[monitor_thread] returned failed termination string.'
                            'returning gathered samples and exiting.')

                        statistics['throughput_responses_sec'] = -1
                        samples.append(statistics)
                        result_queue.put(samples, block=True)
                        return

                    if match is not None:

                        # extract the numeric portion from the above regex
                        statistics['throughput_responses_sec'] = \
                            float(match.group(1)) * 1000.0

                        samples.append(statistics)
                    internal_repeat_id += 1

        except queue.Empty as exept:
            logging.error('[monitor_thread] {0}'.format(str(exept)))


def sb_active_stability_cbench_run(out_json, ctrl_base_dir, sb_gen_base_dir,
                                   conf, output_dir):
    """Run test. This is the main function that is called from
    nstat_orchestrator and performs the specific test.

    :param out_json: the JSON output file
    :param ctrl_base_dir: controller base directory
    :param sb_gen_base_dir: Cbench base directory
    :param conf: JSON configuration dictionary
    :param output_dir: directory to store output files
    :type out_json: str
    :type ctrl_base_dir: str
    :type sb_gen_base_dir: str
    :type conf: str
    :type output_dir: str
    """

    test_type = '[sb_active_stability_cbench]'
    logging.info('{0} initializing test parameters'.format(test_type))

    # Cbench parameters: multiprocessing objects
    cbench_threads = multiprocessing.Value('i', 0)
    cbench_switches_per_thread = multiprocessing.Value('i', 0)
    cbench_thread_creation_delay_ms = multiprocessing.Value('i', 0)
    cbench_delay_before_traffic_ms = multiprocessing.Value('i', 0)
    cbench_simulated_hosts = multiprocessing.Value('i', 0)
    cbench_switches = multiprocessing.Value('i', 0)

    # Various parameters: multiprocessing objects
    repeat_id = multiprocessing.Value('i', 0)
    controller_statistics_period_ms = multiprocessing.Value('i', 0)
    cpid = multiprocessing.Value('i', 0)
    global_sample_id = multiprocessing.Value('i', 0)

    cbench_rebuild = conf['cbench_rebuild']
    cbench_cleanup = conf['cbench_cleanup']
    cbench_name = conf['cbench_name']
    if 'mtcbench_cpu_shares' in conf:
        mtcbench_cpu_shares = conf['mtcbench_cpu_shares']
    else:
        mtcbench_cpu_shares = 100

    cbench_ms_per_test = conf['cbench_ms_per_test']
    cbench_internal_repeats = conf['cbench_internal_repeats']
    cbench_warmup = conf['cbench_warmup']
    cbench_mode = conf['cbench_mode']

    # Controller parameters
    controller_logs_dir = ctrl_base_dir + conf['controller_logs_dir']
    controller_rebuild = conf['controller_rebuild']
    controller_cleanup = conf['controller_cleanup']
    if 'controller_cpu_shares' in conf:
        controller_cpu_shares = conf['controller_cpu_shares']
    else:
        controller_cpu_shares = 100

    # Shared read-write variables between monitor-main thread and Cbench thread.
    test_repeats = conf['test_repeats']
    java_opts = conf['java_opts']

    controller_node = conf_collections_util.node_parameters('Controller',
                                      conf['controller_node_ip'],
                                      int(conf['controller_node_ssh_port']),
                                      conf['controller_node_username'],
                                      conf['controller_node_password'])
    cbench_node = conf_collections_util.node_parameters('MT-Cbench',
                                   conf['cbench_node_ip'],
                                   int(conf['cbench_node_ssh_port']),
                                   conf['cbench_node_username'],
                                   conf['cbench_node_password'])
    controller_handlers_set = conf_collections_util.controller_handlers(
        ctrl_base_dir + conf['controller_build_handler'],
        ctrl_base_dir + conf['controller_start_handler'],
        ctrl_base_dir + conf['controller_status_handler'],
        ctrl_base_dir + conf['controller_stop_handler'],
        ctrl_base_dir + conf['controller_clean_handler'],
        ctrl_base_dir + conf['controller_statistics_handler']
        )
    cbench_handlers_set = conf_collections_util.cbench_handlers(
        sb_gen_base_dir + conf['cbench_build_handler'],
        sb_gen_base_dir + conf['cbench_clean_handler'],
        sb_gen_base_dir + conf['cbench_run_handler'])

    controller_sb_interface = \
        conf_collections_util.controller_southbound(conf['controller_node_ip'],
                                                    conf['controller_port'])

    # termination message sent to monitor thread when Cbench is finished
    term_success = '__successful_termination__'
    term_fail = '__failed_termination__'

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

        # Opening connection with cbench_node_ip and returning
        # cbench_ssh_client to be utilized in the sequel
        cbench_ssh_client, controller_ssh_client = \
            common.open_ssh_connections([cbench_node, controller_node])

        controller_cpus, cbench_cpus = common.create_cpu_shares(
            controller_cpu_shares, mtcbench_cpu_shares)

        if cbench_rebuild:
            logging.info('{0} building cbench.'.format(test_type))
            cbench_utils.rebuild_cbench(
                cbench_handlers_set.cbench_build_handler, cbench_ssh_client)

        # Controller common actions:
        # 1. rebuild controller if controller_rebuild is SET
        # 2. check_for_active controller,
        # 3. generate_controller_xml_files

        controller_utils.controller_pre_actions(controller_handlers_set,
                                      controller_rebuild, controller_ssh_client,
                                      java_opts, controller_sb_interface.port,
                                      controller_cpus)

        # run tests for all possible dimensions
        for (cbench_threads.value,
             cbench_switches_per_thread.value,
             cbench_thread_creation_delay_ms.value,
             cbench_delay_before_traffic_ms.value,
             cbench_simulated_hosts.value,
             repeat_id.value,
             controller_statistics_period_ms.value) in \
             itertools.product(conf['cbench_threads'],
                               conf['cbench_switches_per_thread'],
                               conf['cbench_thread_creation_delay_ms'],
                               conf['cbench_delay_before_traffic_ms'],
                               conf['cbench_simulated_hosts'],
                               list(range(0, test_repeats)),
                               conf['controller_statistics_period_ms']):

            logging.info('{0} changing controller statistics period to {1} ms'.
                format(test_type, controller_statistics_period_ms.value))
            controller_utils.controller_changestatsperiod(
                controller_handlers_set.ctrl_statistics_handler,
                controller_statistics_period_ms.value, controller_ssh_client)

            logging.info('{0} starting controller'.format(test_type))
            cpid.value = controller_utils.start_controller(
                controller_handlers_set, controller_sb_interface.port,
                ' '.join(conf['java_opts']), controller_cpus,
                controller_ssh_client)
            logging.info('{0} OK, controller status is 1.'.format(test_type))

            cbench_switches.value = \
                cbench_threads.value * cbench_switches_per_thread.value

            logging.info('{0} creating data and result queues'.
                          format(test_type))
            data_queue = multiprocessing.Queue()
            result_queue = multiprocessing.Queue()

            logging.info('{0} creating monitor thread'.format(test_type))
            monitor_thread = multiprocessing.Process(
                target=monitor, args=(data_queue, result_queue,
                                      cpid, global_sample_id, repeat_id,
                                      test_repeats,
                                      cbench_switches,
                                      cbench_switches_per_thread,
                                      cbench_threads,
                                      cbench_delay_before_traffic_ms,
                                      cbench_thread_creation_delay_ms,
                                      cbench_simulated_hosts,
                                      cbench_ms_per_test,
                                      cbench_internal_repeats,
                                      cbench_warmup, cbench_mode,
                                      mtcbench_cpu_shares,
                                      controller_statistics_period_ms,
                                      controller_sb_interface.port,
                                      controller_node,
                                      controller_cpu_shares,
                                      term_success, term_fail))

            logging.info('{0} creating cbench thread'.format(test_type))
            cbench_thread = multiprocessing.Process(
                target=cbench_utils.cbench_thread,
                args=(cbench_handlers_set.cbench_run_handler,
                      cbench_cpus, controller_node.ip,
                      controller_sb_interface.port, cbench_threads,
                      cbench_switches_per_thread,
                      cbench_switches,
                      cbench_thread_creation_delay_ms,
                      cbench_delay_before_traffic_ms,
                      cbench_ms_per_test, cbench_internal_repeats,
                      cbench_simulated_hosts, cbench_warmup,
                      cbench_mode,
                      cbench_node, term_success, term_fail,
                      data_queue))

            # parallel section: starting monitor/cbench threads
            monitor_thread.start()
            cbench_thread.start()

            samples = result_queue.get(block=True)
            total_samples = total_samples + samples
            logging.info('{0} joining monitor thread'.format(test_type))
            monitor_thread.join()
            logging.info('{0} joining cbench thread'.format(test_type))
            cbench_thread.join()

            controller_utils.stop_controller(controller_handlers_set,
                                             cpid.value, controller_ssh_client)

    except:
        logging.error('{0} :::::::::: Exception caught :::::::::::'.
                      format(test_type))
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
            controller_utils.stop_controller(controller_handlers_set,
                                             cpid.value, controller_ssh_client)
        except:
            pass

        try:
            logging.info('{0} collecting logs'.format(test_type))
            util.netutil.copy_dir_remote_to_local(controller_node,
                controller_logs_dir, output_dir + '/log')
        except:
            logging.error('{0} {1}'.format(
                test_type, 'failed transferring controller logs directory.'))

        if controller_cleanup:
            logging.info('{0} cleaning controller build directory.'.
                         format(test_type))
            controller_utils.cleanup_controller(
                controller_handlers_set.ctrl_clean_handler,
                controller_ssh_client)

        if cbench_cleanup:
            logging.info('{0} cleaning cbench build directory.'.
                         format(test_type))
            cbench_utils.cleanup_cbench(
                cbench_handlers_set.cbench_clean_handler, cbench_ssh_client)

        # closing ssh connections with controller/cbench nodes
        common.close_ssh_connections([controller_ssh_client, cbench_ssh_client])


def get_report_spec(test_type, config_json, results_json):
    """It returns all the information that is needed for the generation of the
    report for the specific test.

    :param test_type: describes the type of the specific test. This value
    defines the title of the html report.
    :param config_json: This is the filepath to the configuration json file.
    :param results_json: This is the filepath to the results json file.
    :returns: A ReportSpec object that holds all the test report information
    and is passed as input to the generate_html() function in the
    html_generation.py, that is responsible for the report generation.
    :rtype: ReportSpec
    :type: test_type: str
    :type: config_json: str
    :type: results_json: str
    """

    report_spec_obj = report_spec.ReportSpec(
        config_json, results_json, '{0}'.format(test_type),
        [report_spec.TableSpec(
            '1d', 'Test configuration parameters (detailed)',
            [('test_repeats', 'Test repeats'),
             ('controller_name', 'Controller name'),
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
              'Switches per generator thread'),
             ('cbench_internal_repeats', 'Generator internal repeats'),
             ('cbench_ms_per_test', 'Internal repeats duration in ms'),
             ('cbench_rebuild',
              'Generator rebuild between each test repeat'),
             ('cbench_mode', 'Generator testing mode'),
             ('cbench_warmup', 'Generator warmup repeats'),
             ('cbench_delay_before_traffic_ms',
              'Generator delay before sending traffic in ms'),
             ('java_opts', 'JVM options')
            ], config_json)],
        [report_spec.TableSpec('2d', 'Test results',
            [('global_sample_id', 'Sample ID'),
             ('timestamp', 'Sample timestamp (seconds)'),
             ('date', 'Sample timestamp (date)'),
             ('test_repeats', 'Total test repeats'),
             ('repeat_id', 'External repeat ID'),
             ('cbench_internal_repeats', 'Generator Internal repeats'),
             ('internal_repeat_id', 'Internal repeat ID'),
             ('throughput_responses_sec', 'Throughput (responses/sec)'),
             ('cbench_simulated_hosts', 'Generator simulated hosts'),
             ('cbench_switches', 'Generated simulated switches'),
             ('cbench_threads', 'Generator threads'),
             ('cbench_switches_per_thread',
              'Switches per generator thread'),
             ('cbench_thread_creation_delay_ms',
              'Delay between thread creation (ms)'),
             ('cbench_delay_before_traffic_ms',
              'Delay before PacketIn transmission (ms)'),
             ('cbench_ms_per_test', 'Internal repeats interval'),
             ('cbench_warmup', 'Cbench warmup repeats'),
             ('cbench_mode', 'Cbench test mode'),
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
              'Controller statistics period (ms)')
            ], results_json)])
    return report_spec_obj
