# Copyright (C) 2016 Petr Horacek <phoracek@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import subprocess


PING4 = 'ping'
PING6 = 'ping6'


class ConnectivityCheckError(Exception):
    pass


def check_ping(parameters):
    check_parameters = parameters.get('connectivitycheck_ping')
    if check_parameters is not None:
        address = check_parameters['address']
        timeout = check_parameters['timeout']
        logging.info('Running connecitivity check on address {} with timeout '
                     '{}'.format(address, timeout))
        _check_ping(address, timeout)
        logging.info('Ping connectivity check finished')
    else:
        logging.info('Ping connectivity check disabled')


def _check_ping(address, timeout):
    time_start = _time()
    while True:
        time_passed = _time() - time_start
        if time_passed > timeout:
            raise ConnectivityCheckError('Ping connectivity check failed')
        if _ping(address, timeout - time_passed):
            return


def _ping(address, timeout):
    try:
        ping = PING6 if ':' in address else PING4
        subprocess.run(
            [ping, '-q', '-c', '1', address], timeout=timeout, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    else:
        return True


def _time():
    return os.times()[4]
