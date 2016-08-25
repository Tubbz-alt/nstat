# Copyright (c) 2016 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

""" Controller Class- All controller-related functionality is here"""

import json
import common
import logging
import os
import subprocess
import time
import util.netutil
import util.process

class Controller:

    def __init__(self, ctrl_base_dir, test_config):

        """Create a Controller object. Options from JSON input file
        :param test_config: JSON input configuration
        :param ctrl_base_dir: controller base directory
        :type test_config: JSON configuration dictionary
        :type ctrl_base_dir: str
        """
        self.name = test_config['controller_name']
        self.base_dir = ctrl_base_dir

        self.ip = test_config['controller_node_ip']
        self.ssh_port = test_config['controller_node_ssh_port']
        self.ssh_user = test_config['controller_node_username']
        self.ssh_pass = test_config['controller_password']

        self.need_rebuild = self.base_dir + test_config['controller_rebuild']
        self.need_cleanup = self.base_dir + test_config['controller_cleanup']
        self.of_port = test_config['controller_port']
        self.logs_dir = self.base_dir + test_config['controller_logs_dir']

        self.build_hnd = self.base_dir + test_config['controller_build_handler']
        self.start_hnd = self.base_dir + test_config['controller_start_handler']
        self.stop_hnd = self.base_dir + test_config['controller_stop_handler']
        self.status_hnd = self.base_dir + test_config['controller_status_handler']
        self.clean_hnd = self.base_dir + test_config['controller_clean_handler']

        self.status = 'UNKNOWN'

        self.java_opts = ' '.join(test_config['java_opts'])
        self.pid = -1

        self.ssh_pass = None


    def init_ssh(self)
        logging.info(
            '[open_ssh_connection] Initiating SSH session with {0} node.'.
            format(self.name, self.ip))
        self.ssh_pass = util.netutil.__ssh_connect_or_return(self.ip,
                                      int(self.ssh_port),
                                      self.ssh_user,
                                      self.ssh_pass,
                                      10)


    def cleanup(self):
        """Wrapper to the controller cleanup handler
        """
        logging.info('[Controller] Cleaning up')

        self.status = 'CLEANING'
        common.command_exec_wrapper([self.clean_hnd],
                                    '[controller.clean_handler]', self.ssh_pass)
        self.status = 'CLEANED'

    def check_status(self):
        """Wrapper to the controller status handler
        """
        logging.info('[Controller] Checking the status')

        common.command_exec_wrapper([self.status_hnd],
                                    '[controller_status_handler]',
                                    self.status_hnd)


    def check_other_controller(self):
        """Checks for processes listening on the specified port

        :raises Exception: when another process listens on controller's port.
        """

        logging.info(
            '[Controller] Checking if another process is '
            'listening on specified port. Port number: {0}.'.
            format(self.of_port))

        # check if any process listens on controller port
        gpid = util.process.getpid_listeningonport(self.of_port, self.ssh_pass)

        if gpid != -1:
            raise Exception('[check_other_controller] Another process is '
                            'active on port {0}'.
                            format(self.of_port))

    def restart(self):
        """Restarts the controller
        :rtype: int
        """
        logging.info('[Controller] Restarting')

        self.status = 'RESTARTING'
        self.stop()
        self.pid = self.start()
        self.status = 'RESTARTED'

    def start(self):
        """Wrapper to the controller start handler
        :raises Exception: When controller fails to start.
        :rtype: int
        """
        logging.info('[Controller] Starting')

        self.status = 'STARTING'
        if self.ssh_pass==None:
            os.environ['JAVA_OPTS'] = self.java_opts
            cmd = [self.start_hnd]
        else:
            cmd = ['export JAVA_OPTS="{0}";'.format(self.java_opts),
                   self.start_hnd]

        if check_status() == '0':
            common.command_exec_wrapper(cmd, '[controller_start_handler]', self.ssh_pass)
            logging.info(
                '[start_controller] Waiting until controller starts listening')
            self.pid = self.wait_until_listens(420000)
            logging.info('[start_controller] Controller pid: {0}'.format(self.pid))
            logging.info(
                '[start_controller] Checking controller status after it starts '
                'listening on port {0}.'.format(self.of_port))
            self.wait_until_up(420000)
        else:
            logging.info('[start_controller] Controller already started.')

        self.status = 'STARTED'

    def stop(self):
        """Wrapper to the controller stop handler
        """

        self.status = 'STOPPING'
        if check_status() == '1':
            logging.info('[stop_controller] Stopping controller.')
            common.command_exec_wrapper(
                [self.stop_hnd],
                '[controller_stop_handler]', self.ssh_pass)
            util.process.wait_until_process_finishes(self.pid, self.ssh_pass)
            self.status = 'STOPPED'

            else:
            logging.info('[stop_controller] Controller already stopped.')

    def build(self):
        """ Wrapper to the controller build handler
        """
        logging.info('[Controller] Building')
        self.status = 'BUILDING'

        common.command_exec_wrapper([self.build_hnd],
                             '[controller_build_handler]', self.ssh_pass)

        self.status = 'BUILT'

    def wait_until_listens(self,timeout_ms):
        """ Waits for controller to start listening on specified port.

        :param timeout_ms: milliseconds to wait (in milliseconds).
        :raises Exception: If controller fails to start or if another process
        listens on controllers port.
        :rtype int
        :type timeout_ms: int
        """

        logging.info('[Controller] Waiting to start listening on a port')

        timeout = time.time() + (float(timeout_ms) / 1000)
        while time.time() < timeout:
            time.sleep(1)
            gpid = util.process.getpid_listeningonport(self.port, self.ssh_pass)
            logging.info('Returned pid listening on port {0}: {1}'.
                          format(self.port, gpid))
            if gpid == 0:
                raise Exception('Another controller seems to have started in the '
                                'meantime. Exiting...')

        raise Exception('Controller failed to start within a period of {0} '
                        'minutes'.format(timeout))


    def wait_until_up(self,timeout_ms):
        """ Waits for controller status to become 1 (started).

        :param timeout_ms: milliseconds to wait (in milliseconds).
        :raises Exception: If controller fails to start or if another process
        listens on controllers port.
        :type timeout_ms: int
        """

        logging.info('[Controller] Waiting to be started')

        timeout = time.time() + (float(timeout_ms) / 1000)
        while time.time() < timeout:
            time.sleep(1)
            if check_status() == '1':
                return

        raise Exception('Controller failed to start. '
                        'Status check returned 0 after trying for {0} seconds.'.
                        format(float(timeout_ms) / 1000))


    @staticmethod
    def new_controller(self)
        """ Factory method. Creates a subclass class depending on the controller name
        :returns: a subclass or None
        :rtype: failed_flow_ops int
        """

        if (self.name == 'OLD'):
           return ODL()
        elif (self.name == 'ONOS'):
           return ONOS()
        else:
            return None


class ODL(Controller):

    def __init__(self, ctrl_base_dir, test_config):

        super(self.__class__, self).__init__(ctrl_base_dir, test_config)

        self.stat_period_ms = test_config['controller_statistics_period_ms']

        if 'controller_flowmods_conf_handler' in test_config:
            self.flowmods_conf_hnd= ctrl_base_dir + test_config['controller_flowmods_conf_handler']

        if 'controller_statistics_handler' in test_config:
            self.statistics_hnd = ctrl_base_dir + test_config['controller_statistics_handler']

        if 'controller_persistent_handler' in test_config:
            self.persistent_hnd = ctrl_base_dir + test_config['controller_persistent_handler']

        if 'controller_restconf_port' in test_config:
            self.restconf_port = test_config['controller_restconf_port']
            self.restconf_user = test_config['controller_restconf_user']
            self.restconf_password = test_config['controller_restconf_password']

        self.oper_hosts = -1
        self.oper_switches = -1
        self.oper_links = -1
        self.oper_flows = -1


    def generate_xmls(self):
        """ Starts and then stops the controller to trigger the generation of
        controller's XML files.
        """
        logging.info('[Controller] Generating XMLs')
        pid = self.start()
        self.stop()


    def disable_persistence(self):
        """configure controller persistent to false in order not to backup
        datastore on the disk.
        """
        logging.info('[controller] Disabling persistence')

        common.command_exec_wrapper([self.persistent_hnd],
                                    '[controller_change_persistent_handler]',
                                    self.ssh_pass)


    def change_stats(self):
        """Wrapper to the controller statistics handler
        """

        logging.info('[controller] Changing statistics period')
        common.command_exec_wrapper(
            [self.statistics_hnd, str(self.stat_period_ms)],
            '[controller.statistics_handler] Changing statistics interval',
            self.ssh_pass)
        logging.info(
            '[change_stats] Changed statistics period to {0} ms'.
            format(self.stat_period_ms))


    def flowmods_config(self):
        """configure controller to send flow modifications as a responce to ARP
        Packet_INs.
        """
        logging.info('[controller] Configure flow modifications')
        common.command_exec_wrapper([self.flowmods_conf_hnd],
                                    '[controller_flowmod_configure_handler]',
                                    self.ssh_pass)


    def get_oper_hosts(self):
        """Wrapper to the controller oper_hosts handler
        """

    def get_oper_switches(self):
        """Wrapper to the controller oper_switches handler
        """


    def get_oper_links(self):
        """Wrapper to the controller oper_links handler
        """


    def get_oper_flows(self):
        """Wrapper to the controller oper_flows handler
        """


class ONOS(Controller):

    def __init__(self, ctrl_base_dir, test_config):

        super(self.__class__, self).__init__(ctrl_base_dir, test_config)

        self.stat_period_ms = test_config['controller_statistics_period_ms']

        self.oper_hosts = -1
        self.oper_switches = -1
        self.oper_links = -1
        self.oper_flows = -1