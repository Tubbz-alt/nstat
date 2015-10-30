# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

""" Reusable functions for processes that are controller related """

import common
import logging
import subprocess
import time
import util.customsubprocess
import util.netutil
import util.process


def command_exec_wrapper(cmd_list, prefix='', ssh_client=None,
                         data_queue=None):
    """Executes a command either locally or remotely and returns the result

    :param cmd_list: the command to be executed given in a list format of
    command and its arguments
    :param prefix: The prefix to be used for logging of executed command output
    :param ssh_client : SSH client provided by paramiko to run the command
    :param data_queue: data queue where generator output is posted line by line
    the generator process will run.
    :returns: The commands exit status
    :rtype: int
    :type cmd_list: list<str>
    :type prefix: str
    :type ssh_client: paramiko.SSHClient
    :type data_queue: multiprocessing.Queue
    """

    if ssh_client == None:
        exit_status = util.customsubprocess.check_output_streaming(cmd_list,
            prefix, data_queue)
    else:
        exit_status, cmd_output = util.netutil.ssh_run_command(ssh_client,
            ' '.join(cmd_list), prefix, data_queue)
    return exit_status



def rebuild_controller(controller_build_handler, ssh_client=None):
    """ Wrapper to the controller build handler

    :param controller_build_handler: filepath to the controller build handler
    :param ssh_client : SSH client provided by paramiko to run the command
    :type controller_build_handler: str
    :type ssh_client: paramiko.SSHClient
    """

    command_exec_wrapper([controller_build_handler],
                         '[controller_build_handler]', ssh_client)

def start_controller(controller_start_handler, controller_status_handler,
                     controller_port, controller_cpus_str, ssh_client=None):
    """Wrapper to the controller start handler

    :param controller_start_handler: filepath to the controller start handler
    :param controller_status_handler: filepath to the controller status handler
    :param controller_port: controller port number to listen for SB connections
    :param controller_cpus_str: controller CPU share as a strin containing
    the values of shares, separated with coma
    :param ssh_client : SSH client provided by paramiko to run the command
    :returns: controller's process ID
    :raises Exception: When controller fails to start.
    :rtype: int
    :type controller_start_handler: str
    :type controller_status_handler: str
    :type controller_port: int
    :type controller_cpus_str: str
    :type ssh_client: paramiko.SSHClient
    """

    if check_controller_status(controller_status_handler, ssh_client) == '0':
        command_exec_wrapper(
            ['taskset', '-c', controller_cpus_str, controller_start_handler],
            '[controller_start_handler]', ssh_client)
        logging.info(
            '[start_controller] Waiting until controller starts listening')
        cpid = wait_until_controller_listens(420000, controller_port,
                                             ssh_client)
        logging.info('[start_controller] Controller pid: {0}'.format(cpid))
        logging.info(
            '[start_controller] Checking controller status after it starts '
            'listening on port {0}.'.format(controller_port))
        wait_until_controller_up_and_running(420000,
                                             controller_status_handler,
                                             ssh_client)
        return cpid
    else:
        logging.info('[start_controller] Controller already started.')


def cleanup_controller(controller_clean_handler, ssh_client=None):
    """Wrapper to the controller cleanup handler

    :param controller_clean_handler: filepath to the controller cleanup handler
    :param ssh_client : SSH client provided by paramiko to run the command
    :type controller_clean_handler: str
    :type ssh_client: paramiko.SSHClient
    """
    command_exec_wrapper([controller_clean_handler],
                         '[controller_clean_handler]')

def stop_controller(controller_stop_handler, controller_status_handler, cpid,
                    ssh_client=None):
    """Wrapper to the controller stop handler


    :param controller_stop_handler: filepath to the controller stop handler
    :param controller_status_handler: filepath to the controller status handler
    :param cpid: controller process ID
    :param ssh_client : SSH client provided by paramiko to run the command
    :type controller_stop_handler: str
    :type controller_status_handler: str
    :type cpid: int
    :type ssh_client: paramiko.SSHClient
    """

    if check_controller_status(controller_status_handler, ssh_client) == '1':
        logging.info('[stop_controller] Stopping controller.')
        command_exec_wrapper(
            [controller_stop_handler], '[controller_stop_handler]')
        util.process.wait_until_process_finishes(cpid, ssh_client)
    else:
        logging.info('[stop_controller] Controller already stopped.')


def check_controller_status(controller_status_handler, ssh_client=None):
    """Wrapper to the controller status handler

    :param controller_status_handler: filepath to the controller status handler
    :param ssh_client : SSH client provided by paramiko to run the command
    :returns: '1' if controller is active, '0' otherwise
    :rtype: str
    :type controller_status_handler: str
    :type ssh_client: paramiko.SSHClient
    """

    if ssh_client == None:
        return subprocess.check_output([controller_status_handler],
                                   universal_newlines=True).strip()
    else:
        exit_status, cmd_output = ssh_run_command(ssh_client,
            [controller_status_handler])
        return cmd_output.strip()

def controller_changestatsperiod(controller_statistics_handler,
                                 stat_period_ms, ssh_client=None):
    """Wrapper to the controller statistics handler

    :param controller_statistics_handler: filepath to the controller statistics
    handler
    :param stat_period_ms: statistics period value to set (in milliseconds)
    :param ssh_client : SSH client provided by paramiko to run the command
    :type controller_statistics_handler: str
    :type curr_stat_period: int
    :type ssh_client: paramiko.SSHClient
    """
    command_exec_wrapper(
        [controller_statistics_handler, str(stat_period_ms)],
        '[controller_statistics_handler] Changing statistics interval',
        ssh_client)
    logging.info(
        '[controller_changestatsperiod] Changed statistics period to {0} ms'.
        format(stat_period_ms))


def restart_controller(controller_stop_handler, controller_start_handler,
                       controller_status_handler, controller_port, old_cpid,
                       controller_cpus_str, ssh_client=None):
    """Restarts the controller

    :param controller_start: filepath to the controller start handler
    :param controller_status: filepath to the controller status handler
    :param controller_stop: filepath to the controller stop handler
    :param controller_port: controller port number to listen for SB connections
    :param old_cpid: PID of already running controller process
    :param controller_cpus_str: controller CPU share as a strin containing
    the values of shares, separated with comma
    :param ssh_client : SSH client provided by paramiko to run the command
    :returns: controller process ID
    :rtype: int
    :type controller_start: str
    :type controller_status: str
    :type controller_stop: str
    :type controller_port: int
    :type old_cpid: int
    :type controller_cpus_str: str
    :type ssh_client: paramiko.SSHClient
    """

    stop_controller(controller_stop_handler, controller_status_handler,
                    old_cpid, ssh_client)
    new_cpid = start_controller(controller_start_handler,
        controller_status_handler, controller_port, controller_cpus_str,
        ssh_client)
    return new_cpid


def check_for_active_controller(controller_port, ssh_client=None):
    """Checks for processes listening on the specified port

    :param controller_port: controller port to check
    :param ssh_client : SSH client provided by paramiko to run the command
    :raises Exception: When another process Listens on controller's port.
    :type controller_port: int
    :type ssh_client: paramiko.SSHClient
    """

    logging.info(
        '[check_for_active_controller] Checking if another process is '
        'listening on specified port. Port number: {0}.'.
        format(controller_port))

    cpid = util.process.getpid_listeningonport(controller_port, ssh_client)

    if cpid != -1:
        raise Exception('[check_for_active_controller] Another process is '
                        'active on port {0}'.
                        format(controller_port))
    return cpid


def wait_until_controller_listens(interval_ms, port, ssh_client=None):
    """ Waits for the controller to start listening on specified port.

    :param interval_ms: milliseconds to wait (in milliseconds).
    :param port: controller port.
    :param ssh_client : SSH client provided by paramiko to run the command
    :raises Exception: If controller fails to start or if another process
    listens on controllers port.
    :returns: on success, returns the controller pid.
    :rtype int
    :type interval_ms: int
    :type port: int
    :type ssh_client: paramiko.SSHClient
    """

    timeout = time.time() + (float(interval_ms) / 1000)
    while time.time() < timeout:
        time.sleep(1)
        pid = util.process.getpid_listeningonport(port, ssh_client)
        logging.info('Returned pid listening on port {0}: {1}'.
                      format(port, pid))

        if pid > 0:
            return pid
        elif pid == 0:
            raise Exception('Another controller seems to have started in the '
                            'meantime. Exiting...')

    raise Exception('Controller failed to start within a period of {0} '
                    'minutes'.format(timeout))


def wait_until_controller_up_and_running(interval_ms, controller_status_handler,
                                         ssh_client=None):
    """ Waits for the controller status to become 1 (Started).

    :param interval_ms: milliseconds to wait (in milliseconds).
    :param controller_status_handler: filepath to the controller status handler
    :param ssh_client : SSH client provided by paramiko to run the command
    :raises Exception: If controller fails to start or if another process
    listens on controllers port.
    :type interval_ms: int
    :type controller_status_handler: str
    :type ssh_client: paramiko.SSHClient
    """

    timeout = time.time() + (float(interval_ms) / 1000)
    while time.time() < timeout:
        time.sleep(1)
        if check_controller_status(controller_status_handler, ssh_client) == '1':
            return

    raise Exception('Controller failed to start. '
                    'Status check returned 0 after trying for {0} seconds.'.
                    format(float(interval_ms) / 1000))

