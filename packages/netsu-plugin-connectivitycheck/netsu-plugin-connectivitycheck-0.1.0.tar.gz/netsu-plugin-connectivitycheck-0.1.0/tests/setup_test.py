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

from threading import Thread
import os

import pytest

from netsu_plugin_connectivitycheck import setup


def _check_ping(address, timeout):
    setup.check_ping({'connectivitycheck_ping': {
        'address': address, 'timeout': timeout}})


def _ipv6_enabled():
    SYS_DISABLE_IPV6 = '/proc/sys/net/ipv6/conf/all/disable_ipv6'
    with open(SYS_DISABLE_IPV6) as f:
        return f.read().strip() == '0'


@pytest.mark.unit
class TestPingConnectivityCheck(object):

    def test_disabled_check(self):
        setup.check_ping({})

    def test_address(self):
        _check_ping('localhost', timeout=1)

    def test_ipv4(self):
        _check_ping('127.0.0.1', timeout=1)

    @pytest.mark.skipif(not _ipv6_enabled(), reason='IPv6 is disabled')
    def test_ipv6(self):
        _check_ping('::1', timeout=1)

    def test_invalid_ipv4(self):
        with pytest.raises(setup.ConnectivityCheckError):
            _check_ping('300.300.300.300', timeout=1)

    def test_unavailable_ipv4(self):
        with pytest.raises(setup.ConnectivityCheckError):
            _check_ping('199.199.199.199', timeout=1)

    def test_unavailable_ipv4_timeout(self):
        TIMEOUT = 1

        thread = Thread(target=_check_ping, args=('199.199.199.199', TIMEOUT))
        time_start = os.times()[4]
        thread.start()
        thread.join()
        time_stop = os.times()[4]

        assert time_stop - time_start < TIMEOUT + 0.1
