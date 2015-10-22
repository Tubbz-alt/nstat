import logging
import os
import paramiko
import socket
import stat
import time

import queue

def ssh_run_command(ssh_client, command_to_run, prefix='', lines_queue=None,
                    print_flag=False):
    """Runs the specified command on a remote machine

    :param ssh_client : SSH client provided by paramiko to run the command
    :param command_to_run: Command to execute
    :param lines_queue: Queue datastructure to buffer the result of execution
    :param print_flag: Flag that defines if the output of the command will be
    printed on screen
    :returns: the exit code of the command to be executed remotely and the
    combined stdout - stderr of the executed command
    :rtype: tuple<int, str>
    :type ssh_session: paramiko.SSHClient
    :type command_to_run: str
    :type lines_queue: queue<str>
    """

    channel = ssh_client.get_transport().open_session()
    bufferSize = 4*1024
    channel_timeout = 300 
    channel.setblocking(1)
    channel.set_combine_stderr(True)
    channel.settimeout(channel_timeout)
    try:
        channel.exec_command(command_to_run)
    except SSHException:
        return 1
    channel_output = ''
    while not channel.exit_status_ready():
        try:
            data = ''
            data = channel.recv(bufferSize).decode('utf-8')
            while data:
                channel_output += data
                if print_flag:
                    print('{0} {1}'.format(prefix, data))
                if lines_queue is not None:
                    for line in data.splitlines():
                        lines_queue.put(line)
                data = channel.recv(bufferSize).decode('utf-8')

        except socket.timeout:
            print('{0} Socket timeout exception caught'.format(prefix))
            return 1
        except UnicodeDecodeError:
            # Replace print with logging.error
            print('{0} Decode of received data exception caught'.
                          format(prefix))
            return 1

    channel_exit_status = channel.recv_exit_status()
    channel.close()
    return (channel_exit_status, channel_output)

if __name__ == '__main__':
    S = "this is string example....wow!!!"
    S = S.encode('ASCII','strict')

    print("Encoded String: " + str(S))
    print("Decoded String: " + S.decode('utf-8'))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='127.0.0.1', port=22,
                        username='jenkins', password='jenkins')
    cmd = 'ls -la'
    exit_status, output = ssh_run_command(ssh_client, cmd, '[Functional_test] ', None, True)
    print('PRINTING RETURNED OUTPUT: \n'+output)

    cmd = '''echo "This is on stderr" >&2 '''
    ssh_run_command(ssh_client, cmd, '[Functional_test] ', None, True)

    cmd = 'echo $HOME'
    ssh_run_command(ssh_client, cmd, '[Functional_test] ', None, True)

    cmd = 'exit 2'
    print('ERROR NUMBER RETURNED: {0}'.format(ssh_run_command(ssh_client, cmd)))

    testing_queue = queue.Queue()
    cmd = 'ls -1'
    print('   === USING QUEUE to buffer results')
    ssh_run_command(ssh_client, cmd, '[Functional_test] ', testing_queue, False)
    print('   === Printing queue buffered results after execution:')
    while not testing_queue.empty():
        print(testing_queue.get())