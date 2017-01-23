# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

import stress_test.report_spec


class TestReport:
    """
    Creates a class for each test includeing the key to be demonstrated
    """
    def __init__(self, test_type, config_json_file):
        """
        Initializes the test_type and json configuration file attributes
        """
        self.test_type = test_type
        self.config_json_file = config_json_file

    def sb_active_scalability_mtcbench(self, results_json_file):
        """
        Returns the report specification for the Southbound active scalability
        test with MT-Cbench

        :param results_json_file: This is the filepath to the results json file
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file, results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('test_repeats', 'Test repeats'),
                 ('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller Southbound port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('sb_emulator_name', 'Generator name'),
                 ('sb_emulator_node_ip', 'Cbench node IP address'),
                 ('sb_emulator_node_ssh_port', 'Cbench node ssh port'),
                 ('sb_emulator_node_username', 'Cbench node username'),
                 ('sb_emulator_node_password', 'Cbench node password'),
                 ('sb_emulator_build_handler', 'Generator build script'),
                 ('mtcbench_run_handler', 'Generator start script'),
                 ('sb_emulator_clean_handler', 'Generator cleanup script'),
                 ('mtcbench_simulated_hosts', 'Generator simulated hosts'),
                 ('mtcbench_threads', 'Generator threads'),
                 ('mtcbench_thread_creation_delay_ms',
                  'Generation delay in ms between thread creation'),
                 ('mtcbench_switches_per_thread',
                  'Switches per generator thread'),
                 ('mtcbench_internal_repeats', 'Generator internal repeats'),
                 ('mtcbench_ms_per_test', 'Internal repeats duration in ms'),
                 ('mtcbench_mode', 'Generator testing mode'),
                 ('mtcbench_warmup', 'Generator warmup repeats'),
                 ('mtcbench_delay_before_traffic_ms',
                  'Generator delay before sending traffic in ms'),
                 ('java_opts', 'JVM options')],
                self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d',
                'Test results',
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
                  'Controller statistics period (ms)')],
                results_json_file)])
        return report_spec_obj

    def sb_active_stability_mtcbench(self, results_json_file):
        """
        Returns the report specification object for SouthBound active
        stabiility test with MT-Cbench.

        :param results_json_file: This is the filepath to the results json file.
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file, results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('test_repeats', 'Test repeats'),
                 ('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller Southbound port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('sb_emulator_name', 'Generator name'),
                 ('sb_emulator_node_ip', 'Cbench node IP address'),
                 ('sb_emulator_node_ssh_port', 'Cbench node ssh port'),
                 ('sb_emulator_node_username', 'Cbench node username'),
                 ('sb_emulator_node_password', 'Cbench node password'),
                 ('sb_emulator_build_handler', 'Generator build script'),
                 ('mtcbench_run_handler', 'Generator start script'),
                 ('sb_emulator_clean_handler', 'Generator cleanup script'),
                 ('mtcbench_simulated_hosts', 'Generator simulated hosts'),
                 ('mtcbench_threads', 'Generator threads'),
                 ('mtcbench_thread_creation_delay_ms',
                  'Generation delay in ms between thread creation'),
                 ('mtcbench_switches_per_thread',
                  'Switches per generator thread'),
                 ('mtcbench_internal_repeats', 'Generator internal repeats'),
                 ('mtcbench_ms_per_test', 'Internal repeats duration in ms'),
                 ('mtcbench_mode', 'Generator testing mode'),
                 ('mtcbench_warmup', 'Generator warmup repeats'),
                 ('mtcbench_delay_before_traffic_ms',
                  'Generator delay before sending traffic in ms'),
                 ('java_opts', 'JVM options')
                 ], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d',
                'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('test_repeats', 'Total test repeats'),
                 ('repeat_id', 'External repeat ID'),
                 ('cbench_internal_repeats',
                 'Generator Internal repeats'),
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
                 ('controller_node_ip',
                  'Controller IP node address'),
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
                  'Controller statistics period (ms)')], results_json_file)])
        return report_spec_obj

    def sb_idle_scalability_mtcbench(self, results_json_file):
        """
        Returns the report specification object for SouthBound idle
        scalability test with MT-Cbench

        :param results_json_file: JSON results path
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file, results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller Southbound port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('sb_emulator_name', 'Generator name'),
                 ('sb_emulator_node_ip', 'Cbench node IP address'),
                 ('sb_emulator_node_ssh_port', 'Cbench node ssh port'),
                 ('sb_emulator_node_username', 'Cbench node username'),
                 ('sb_emulator_node_password', 'Cbench node password'),
                 ('sb_emulator_build_handler', 'Generator build script'),
                 ('mtcbench_run_handler', 'Generator start script'),
                 ('sb_emulator_clean_handler', 'Generator cleanup script'),
                 ('mtcbench_simulated_hosts', 'Generator simulated hosts'),
                 ('mtcbench_threads', 'Generator threads'),
                 ('mtcbench_thread_creation_delay_ms',
                  'Generation delay in ms between thread creation'),
                 ('mtcbench_switches_per_thread',
                  'Switches per cbench thread'),
                 ('mtcbench_internal_repeats', 'Generator internal repeats'),
                 ('mtcbench_ms_per_test', 'Internal repeats duration in ms'),
                 ('mtcbench_mode', 'Generator testing mode'),
                 ('mtcbench_warmup', 'Generator warmup repeats'),
                 ('mtcbench_delay_before_traffic_ms',
                  'Generator delay before sending traffic in ms'),
                 ('java_opts', 'JVM options')], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d',
                'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('cbench_internal_repeats',
                  'Generator Internal repeats'),
                 ('discovered_switches_error_code',
                  'Error code'),
                 ('successful_bootup_time',
                  'Successful bootup time (seconds)'),
                 ('bootup_time_secs',
                  'Time to discover switches (seconds)'),
                 ('max_discovered_switches',
                  'Max discovered switches'),
                 ('discovered_switches',
                  'Discovered switches'),
                 ('cbench_simulated_hosts',
                  'Generator simulated hosts'),
                 ('cbench_switches',
                  'Generated simulated switches'),
                 ('cbench_threads', 'Generator threads'),
                 ('cbench_switches_per_thread',
                  'Switches per cbench thread'),
                 ('cbench_thread_creation_delay_ms',
                  'Delay between thread creation (ms)'),
                 ('cbench_delay_before_traffic_ms',
                  'Delay before PacketIn transmission (ms)'),
                 ('cbench_ms_per_test',
                  'Internal repeats interval'),
                 ('cbench_warmup', 'Generator warmup repeats'),
                 ('cbench_mode', 'Generator test mode'),
                 ('mtcbench_cpu_shares',
                  'MT-Cbench CPU percentage'),
                 ('controller_node_ip',
                  'Controller IP node address'),
                 ('controller_port', 'Controller port'),
                 ('controller_java_xopts', 'Java options'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'five minutes load'),
                 ('fifteen_minute_load',
                  'fifteen minutes load'),
                 ('used_memory_bytes',
                  'System used memory (Bytes)'),
                 ('total_memory_bytes', 'Total system memory'),
                 ('controller_cpu_shares',
                  'Controller CPU percentage'),
                 ('controller_cpu_system_time',
                  'Controller CPU system time'),
                 ('controller_cpu_user_time',
                  'Controller CPU user time'),
                 ('controller_num_threads',
                  'Controller threads'),
                 ('controller_num_fds',
                  'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller statistics period (ms)')],
                results_json_file)])
        return report_spec_obj

    def sb_active_scalability_multinet(self, results_json_file):
        """
        Returns the report specification object for SouthBound active
        scalability test with Multinet

        :param results_json_file: This is the filepath to the results json file.
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """
        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file, results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('test_repeats', 'Test repeats'),
                 ('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller listening port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('topology_rest_server_boot', 'Multinet boot handler'),
                 ('topology_stop_switches_handler',
                  'Multinet stop switches handler'),
                 ('topology_get_switches_handler',
                  'Multinet get switches handler'),
                 ('topology_init_handler',
                  'Multinet initialize topology handler'),
                 ('topology_start_switches_handler',
                  'Multinet start topology handler'),
                 ('sb_emulator_node_ip', 'Multinet IP address'),
                 ('topology_rest_server_port', 'Multinet port'),
                 ('multinet_topo_size', 'Multinet network size per worker'),
                 ('multinet_topo_type', 'Multinet topology type'),
                 ('multinet_topo_hosts_per_switch',
                  'Multinet hosts per switch'),
                 ('multinet_topo_group_size', 'Multinet topology group size'),
                 ('multinet_topo_group_delay_ms',
                  'Multinet topology group delay ms'),
                 ('java_opts', 'JVM options')], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d',
                'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('test_repeats', 'Total test repeats'),
                 ('repeat_id', 'External repeat ID'),
                 ('of_out_bytes_per_sec',
                  'Outgoing controller throughput '
                  '(Bytes per second)'),
                 ('of_in_bytes_per_sec',
                  'Incoming controller traffic (Bytes per second)'),
                 ('tcp_of_out_bytes_per_sec',
                  'Outgoing TCP with OpenFlow Payload '
                  'controller throughput (Bytes per second)'),
                 ('tcp_of_in_bytes_per_sec',
                  'Incoming TCP with OpenFlow Payload '
                  'controller traffic (Bytes per second)'),
                 ('traffic_generation_duration_ms',
                  'Traffic generation interval (ms)'),
                 ('interpacket_delay_ms',
                  'Delay between transmitted Packet_INs (ms)'),
                 ('multinet_size', 'Multinet Size'),
                 ('multinet_worker_topo_size',
                  'Topology size per Multinet worker'),
                 ('multinet_workers', 'number of Multinet workers'),
                 ('multinet_topology_type', 'Multinet topology Type'),
                 ('multinet_hosts_per_switch', 'Multinet hosts per Switch'),
                 ('multinet_group_size', 'Multinet group size'),
                 ('multinet_group_delay_ms', 'Multinet group delay (ms)'),
                 ('controller_node_ip', 'Controller IP'),
                 ('controller_port', 'Controller port'),
                 ('controller_java_xopts', 'Java options'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'five minutes load'),
                 ('fifteen_minute_load', 'fifteen minutes load'),
                 ('used_memory_bytes', 'System used memory (Bytes)'),
                 ('total_memory_bytes', 'Total system memory'),
                 ('controller_cpu_system_time', 'Controller CPU system time'),
                 ('controller_cpu_user_time', 'Controller CPU user time'),
                 ('controller_num_threads', 'Controller threads'),
                 ('controller_num_fds', 'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller Statistics Period (ms)')], results_json_file)])
        return report_spec_obj

    def sb_idle_scalability_multinet(self, results_json_file):
        """
        Returns the report specification object for SouthBound idle
        scalability test with Multinet

        :param results_json_file: JSON results path
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file,
            results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d',
                'Test configuration parameters (detailed)',
                [('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller listening port'),
                 ('controller_logs_dir',
                  'Controller log save directory'),
                 ('controller_restconf_port', 'Controller RESTconf port'),
                 ('topology_rest_server_boot', 'Multinet boot handler'),
                 ('topology_stop_switches_handler',
                  'Multinet stop switches handler'),
                 ('topology_get_switches_handler',
                  'Multinet get switches handler'),
                 ('topology_init_handler',
                  'Multinet initialize topology handler'),
                 ('topology_start_switches_handler',
                  'Multinet start topology handler'),
                 ('sb_emulator_node_ip', 'Multinet IP address'),
                 ('topology_rest_server_port', 'Multinet port'),
                 ('multinet_topo_size', 'Multinet network size per worker'),
                 ('multinet_topo_type', 'Multinet topology type'),
                 ('multinet_topo_hosts_per_switch',
                  'Multinet hosts per switch'),
                 ('multinet_topo_group_size', 'Multinet topology group size'),
                 ('multinet_topo_group_delay_ms',
                  'Multinet topology group delay ms'),
                 ('java_opts', 'JVM options')], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d', 'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('discovered_switches_error_code', 'Error code'),
                 ('successful_bootup_time',
                  'Successful bootup time (seconds)'),
                 ('bootup_time_secs', 'Time to discover switches (seconds)'),
                 ('max_discovered_switches', 'Max discovered switches'),
                 ('discovered_switches', 'Discovered switches'),
                 ('multinet_size', 'Multinet Size'),
                 ('multinet_worker_topo_size',
                  'Topology size per Multinet worker'),
                 ('multinet_workers', 'number of Multinet workers'),
                 ('multinet_topology_type', 'Multinet topology Type'),
                 ('multinet_hosts_per_switch', 'Multinet hosts per Switch'),
                 ('multinet_group_size', 'Multinet group size'),
                 ('multinet_group_delay_ms', 'Multinet group delay (ms)'),
                 ('controller_node_ip', 'Controller IP'),
                 ('controller_port', 'Controller port'),
                 ('controller_java_xopts', 'Java options'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'five minutes load'),
                 ('fifteen_minute_load', 'fifteen minutes load'),
                 ('used_memory_bytes', 'System used memory (Bytes)'),
                 ('total_memory_bytes', 'Total system memory'),
                 ('controller_cpu_system_time', 'Controller CPU system time'),
                 ('controller_cpu_user_time', 'Controller CPU user time'),
                 ('controller_num_threads', 'Controller threads'),
                 ('controller_num_fds', 'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller Statistics Period (ms)')], results_json_file)])
        return report_spec_obj

    def sb_idle_stability_multinet(self, results_json_file):
        """
        Returns the report specification object for SouthBound idle
        stability test with Multinet

        :param results_json_file: JSON results path
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file,
            results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('number_of_samples', 'Test repeats'),
                 ('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller listening port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('controller_restconf_port', 'Controller RESTconf port'),
                 ('topology_rest_server_boot', 'Multinet boot handler'),
                 ('topology_stop_switches_handler',
                  'Multinet stop switches handler'),
                 ('topology_get_switches_handler',
                  'Multinet get switches handler'),
                 ('topology_init_handler',
                  'Multinet initialize topology handler'),
                 ('topology_start_switches_handler',
                  'Multinet start topology handler'),
                 ('sb_emulator_node_ip', 'Multinet IP address'),
                 ('topology_rest_server_port', 'Multinet port'),

                 ('multinet_topo_size', 'Multinet network size per worker'),
                 ('multinet_topo_type', 'Multinet topology type'),
                 ('multinet_topo_hosts_per_switch',
                  'Multinet hosts per switch'),
                 ('multinet_topo_group_size', 'Multinet topology group size'),
                 ('multinet_topo_group_delay_ms',
                  'Multinet topology group delay ms'),
                 ('java_opts', 'JVM options')], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d', 'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('of_out_packets_per_sec',
                  'Openflow outgoing packets per second'),
                 ('of_out_bytes_per_sec',
                  'Openflow outgoing bytes per second'),
                 ('of_in_packets_per_sec',
                  'Openflow incoming packets per second'),
                 ('of_in_bytes_per_sec',
                  'Openflow incoming bytes per second'),
                 ('tcp_of_out_packets_per_sec',
                  'TCP with Openflow payload outgoing packets per second'),
                 ('tcp_of_out_bytes_per_sec',
                  'TCP with Openflow payload outgoing bytes per second'),
                 ('tcp_of_in_packets_per_sec',
                  'TCP with Openflow payload incoming packets per second'),
                 ('tcp_of_in_bytes_per_sec',
                  'TCP with Openflow payload incoming bytes per second'),
                 ('multinet_size', 'Multinet Size'),
                 ('multinet_worker_topo_size',
                  'Topology size per Multinet worker'),
                 ('multinet_workers', 'Number of Multinet workers'),
                 ('multinet_topology_type', 'Multinet topology Type'),
                 ('multinet_hosts_per_switch', 'Multinet hosts per Switch'),
                 ('multinet_group_size', 'Multinet group size'),
                 ('multinet_group_delay_ms', 'Multinet group delay (ms)'),
                 ('controller_node_ip', 'Controller IP'),
                 ('controller_port', 'Controller port'),
                 ('controller_java_xopts', 'Java options'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'five minutes load'),
                 ('fifteen_minute_load', 'fifteen minutes load'),
                 ('used_memory_bytes', 'System used memory (Bytes)'),
                 ('total_memory_bytes', 'Total system memory'),
                 ('controller_cpu_system_time', 'Controller CPU system time'),
                 ('controller_cpu_user_time', 'Controller CPU user time'),
                 ('controller_num_threads', 'Controller threads'),
                 ('controller_num_fds', 'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller Statistics Period (ms)')], results_json_file)])
        return report_spec_obj

    def nb_active_scalability_multinet(self, results_json_file):
        """
        Returns the report specification object for NorthBound active
        scalability test with Multinet

        :param results_json_file: JSON results path
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file, results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d', 'Test configuration parameters (detailed)',
                [('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_port', 'Controller listening port'),
                 ('controller_logs_dir', 'Controller log save directory'),
                 ('controller_restconf_port', 'Controller RESTconf port'),
                 ('topology_rest_server_boot', 'Multinet boot handler'),
                 ('topology_stop_switches_handler',
                  'Multinet stop switches handler'),
                 ('topology_get_switches_handler',
                  'Multinet get switches handler'),
                 ('topology_init_handler',
                  'Multinet initialize topology handler'),
                 ('topology_start_switches_handler',
                  'Multinet start topology handler'),
                 ('sb_emulator_node_ip', 'Multinet IP address'),
                 ('topology_rest_server_port',
                  'Multinet node REST server port'),
                 ('multinet_topo_size', 'Multinet network size per worker'),
                 ('multinet_topo_type', 'Multinet topology type'),
                 ('multinet_topo_hosts_per_switch', 'Multinet hosts per switch'),
                 ('multinet_topo_group_size', 'Multinet topology group size'),
                 ('multinet_topo_group_delay_ms',
                  'Multinet topology group delay ms'),
                 ('flow_workers', 'Flow worker threads'),
                 ('total_flows', 'Total flows to be added'),
                 ('flow_operations_delay_ms', 'Delay between flow operations'),
                 ('flow_delete_flag', 'Flow delete flag'),
                 ('flows_per_request', 'Flows per REST request'),
                 ('java_opts', 'JVM options')], self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d', 'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('total_flows', 'Total flow operations'),
                 ('total_failed_flows_operations',
                  'Total failed flow operations'),
                 ('add_controller_time', 'Add controller time [s]'),
                 ('add_controller_rate', 'Add controller rate [Flows/s]'),
                 ('add_switch_time', 'Add switch time [s]'),
                 ('add_switch_rate', 'Add switch rate [Flows/s]'),
                 ('add_confirm_time', 'Add confirm time [s]'),
                 ('add_confirm_rate', 'Add confirm rate [Flows/s]'),
                 ('end_to_end_installation_time',
                  'End-to-end installation time [s]'),
                 ('end_to_end_installation_rate',
                  'End-to-end installation rate [Flows/s]'),
                 ('remove_controller_time',
                  'Total time of NB Restconf calls for flows deletion [s]'),
                 ('remove_controller_rate',
                  'Remove controller rate [Flows/s]'),
                 ('remove_switch_time', 'Remove switch time (seconds)'),
                 ('remove_switch_rate', 'Remove switch rate (Flows/seconds)'),
                 ('remove_confirm_time', 'Remove confirm time [s]'),
                 ('remove_confirm_rate', 'Remove confirm rate [Flows/s]'),
                 ('end_to_end_remove_time', 'Delete flows time [s]'),
                 ('end_to_end_remove_rate',
                  'End-to-end remove rate [Flows/s]'),
                 ('flow_operation_delay_ms', 'Flow operation delay [ms]'),
                 ('flow_workers', 'Flow workers'),
                 ('flow_delete_flag', 'Deletion flag'),
                 ('multinet_size', 'Multinet Size'),
                 ('multinet_worker_topo_size',
                  'Topology size per Multinet worker'),
                 ('multinet_workers', 'Number of Multinet workers'),
                 ('multinet_topology_type', 'Multinet topology Type'),
                 ('multinet_hosts_per_switch', 'Multinet hosts per Switch'),
                 ('multinet_group_size', 'Multinet group size'),
                 ('multinet_group_delay_ms', 'Multinet group delay [ms]'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_port', 'Controller port'),
                 ('controller_vm_size', 'Controller VM size'),
                 ('controller_java_xopts', 'Java options'),
                 ('free_memory_bytes', 'System free memory [bytes]'),
                 ('used_memory_bytes', 'System used memory [bytes]'),
                 ('total_memory_bytes', 'System total memory [bytes]'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'Five minutes load'),
                 ('fifteen_minute_load', 'Fifteen minutes load'),
                 ('controller_cpu_system_time', 'Controller CPU system time'),
                 ('controller_cpu_user_time', 'Controller CPU user time'),
                 ('controller_num_threads', 'Controller num of threads'),
                 ('controller_num_fds', 'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller statistics period (ms)')], results_json_file)])
        return report_spec_obj




    def mef_stability_test(self, results_json_file):
        """
        Returns the report specification object for SouthBound idle
        scalability test with Multinet

        :param results_json_file: JSON results path
        :returns: report specification object
        :rtype: ReportSpec
        :type: results_json_file: str
        """

        report_spec_obj = stress_test.report_spec.ReportSpec(
            self.config_json_file,
            results_json_file,
            '{0}'.format(self.test_type),
            [stress_test.report_spec.TableSpec(
                '1d',
                'Test configuration parameters (detailed)',
                [('controller_name', 'Controller name'),
                 ('controller_build_handler', 'Controller build script'),
                 ('controller_start_handler', 'Controller start script'),
                 ('controller_stop_handler', 'Controller stop script'),
                 ('controller_status_handler', 'Controller status script'),
                 ('controller_clean_handler', 'Controller cleanup script'),
                 ('controller_statistics_handler',
                  'Controller statistics script'),
                 ('controller_node_ip', 'Controller IP node address'),
                 ('controller_node_ssh_port', 'Controller node ssh port'),
                 ('controller_node_username', 'Controller node username'),
                 ('controller_node_password', 'Controller node password'),
                 ('controller_port', 'Controller listening port'),
                 ('controller_logs_dir',
                  'Controller log save directory'),
                 ('controller_restconf_port', 'Controller RESTconf port'),
                 ('topology_rest_server_boot', 'Multinet boot handler'),
                 ('topology_stop_switches_handler',
                  'Multinet stop switches handler'),
                 ('topology_get_switches_handler',
                  'Multinet get switches handler'),
                 ('topology_init_handler',
                  'Multinet initialize topology handler'),
                 ('topology_start_switches_handler',
                  'Multinet start topology handler'),
                 ('sb_emulator_node_ip', 'Multinet IP address'),
                 ('topology_rest_server_port', 'Multinet port'),
                 ('multinet_topo_size', 'Multinet network size per worker'),
                 ('multinet_topo_type', 'Multinet topology type'),
                 ('multinet_topo_hosts_per_switch',
                  'Multinet hosts per switch'),
                 ('multinet_topo_group_size', 'Multinet topology group size'),
                 ('multinet_topo_group_delay_ms',
                  'Multinet topology group delay ms'),
                 ('java_opts', 'JVM options'),
                 ('test_repeats', 'Test repeats'),
                 ('test_repeat_interval_ms', 'Test repeat interval (ms)')],
                self.config_json_file)],
            [stress_test.report_spec.TableSpec(
                '2d', 'Test results',
                [('global_sample_id', 'Sample ID'),
                 ('repeat_id', 'Stability repeat ID'),
                 ('timestamp', 'Sample timestamp (seconds)'),
                 ('date', 'Sample timestamp (date)'),
                 ('discovered_switches_error_code', 'Error code'),
                 ('successful_bootup_time',
                  'Successful bootup time (seconds)'),
                 ('bootup_time_secs', 'Time to discover switches (seconds)'),
                 ('max_discovered_switches', 'Max discovered switches'),
                 ('discovered_switches', 'Discovered switches'),
                 ('multinet_size', 'Multinet Size'),
                 ('multinet_worker_topo_size',
                  'Topology size per Multinet worker'),
                 ('multinet_workers', 'number of Multinet workers'),
                 ('multinet_topology_type', 'Multinet topology Type'),
                 ('multinet_hosts_per_switch', 'Multinet hosts per Switch'),
                 ('multinet_group_size', 'Multinet group size'),
                 ('multinet_group_delay_ms', 'Multinet group delay (ms)'),
                 ('controller_node_ip', 'Controller IP'),
                 ('controller_port', 'Controller port'),
                 ('controller_java_xopts', 'Java options'),
                 ('one_minute_load', 'One minute load'),
                 ('five_minute_load', 'five minutes load'),
                 ('fifteen_minute_load', 'fifteen minutes load'),
                 ('used_memory_bytes', 'System used memory (Bytes)'),
                 ('total_memory_bytes', 'Total system memory'),
                 ('controller_cpu_system_time', 'Controller CPU system time'),
                 ('controller_cpu_user_time', 'Controller CPU user time'),
                 ('controller_num_threads', 'Controller threads'),
                 ('controller_num_fds', 'Controller num of fds'),
                 ('controller_statistics_period_ms',
                  'Controller Statistics Period (ms)')], results_json_file)])
        return report_spec_obj
