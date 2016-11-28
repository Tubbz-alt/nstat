# Copyright (c) 2016 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

""" Implementation of custom NB generator exception classes."""


class NBGenError(Exception):
    """Base-class for all NB generator exceptions raised by this module."""
    def __init__(self, err_msg=None, err_code=1):
        self.err_code = err_code
        if err_msg is None:
            Exception.__init__(self, 'NB generator generic exception')
            self.err_msg = 'NB generator generic exception'
        else:
            Exception.__init__(self, err_msg)
            self.err_msg = err_msg


class NBGenNodeConnectionError(NBGenError):
    """A NB generator node connection error."""
    def __init__(self, additional_error_info='', err_code=1):
        NBGenError.__init__(self, 'Fail to establish ssh connection with '
                            'NB generator node. {0}'.
                            format(additional_error_info), err_code)


class NBGenRunError(NBGenError):
    """NB generator run failure."""
    def __init__(self, additional_error_info='', err_code=1):
        NBGenError.__init__(self, 'Fail to run NB generator. {0}'.
                            format(additional_error_info), err_code)


class NBGenPollDSError(NBGenError):
    """NB generator failure during datastore polling."""
    def __init__(self, additional_error_info='', err_code=1):
        NBGenError.__init__(self, 'Fail during datastore polling. {0}'.
                            format(additional_error_info), err_code)


class NBGenPollOVSError(NBGenError):
    """NB generator failure during OpenVSwitch polling."""
    def __init__(self, additional_error_info='', err_code=1):
        NBGenError.__init__(self, 'Fail during OpenVSwitch. {0}'.
                            format(additional_error_info), err_code)


class NBGenMonitorRunError(NBGenError):
    """Error during running monitor threads."""
    def __init__(self, additional_error_info='', err_code=1):
        NBGenError.__init__(self, 'Failure in monitor run. {0}'.
                            format(additional_error_info), err_code)
