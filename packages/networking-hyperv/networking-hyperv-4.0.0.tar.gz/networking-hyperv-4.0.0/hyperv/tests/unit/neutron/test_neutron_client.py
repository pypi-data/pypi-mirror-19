# Copyright 2015 Cloudbase Solutions SRL
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Unit tests for the neutron client.
"""

import mock
from oslo_config import cfg

from hyperv.neutron import constants
from hyperv.neutron import neutron_client
from hyperv.tests import base

CONF = cfg.CONF


class TestNeutronClient(base.BaseTestCase):

    _FAKE_CIDR = '10.0.0.0/24'
    _FAKE_GATEWAY = '10.0.0.1'
    _FAKE_HOST = 'fake_host'

    def setUp(self):
        super(TestNeutronClient, self).setUp()
        self._neutron = neutron_client.NeutronAPIClient()
        self._neutron._client = mock.MagicMock()

    @mock.patch.object(neutron_client.clientv20, "Client")
    def test_init_client(self, mock_client):
        self._neutron._init_client()

        self.assertEqual(mock_client.return_value, self._neutron._client)
        mock_client.assert_called_once_with(
            endpoint_url=CONF.neutron.url,
            timeout=CONF.neutron.url_timeout,
            insecure=True,
            ca_cert=None,
            username=CONF.neutron.admin_username,
            tenant_name=CONF.neutron.admin_tenant_name,
            password=CONF.neutron.admin_password,
            auth_url=CONF.neutron.admin_auth_url,
            auth_strategy=CONF.neutron.auth_strategy)

    def test_get_network_subnets(self):
        self._neutron._client.show_network.return_value = {
            'network': {
                'subnets': [mock.sentinel.fake_subnet]
            }
        }

        subnets = self._neutron.get_network_subnets(mock.sentinel.net_id)

        self._neutron._client.show_network.assert_called_once_with(
            mock.sentinel.net_id)
        self.assertEqual([mock.sentinel.fake_subnet], subnets)

    def test_get_network_subnets_exception(self):
        self._neutron._client.show_network.side_effect = Exception("Fail")
        subnets = self._neutron.get_network_subnets(mock.sentinel.net_id)
        self.assertEqual([], subnets)

    def test_get_network_subnet_cidr(self):
        self._neutron._client.show_subnet.return_value = {
            'subnet': {
                'cidr': self._FAKE_CIDR,
                'gateway_ip': self._FAKE_GATEWAY,
            }
        }

        cidr, gw = self._neutron.get_network_subnet_cidr_and_gateway(
            mock.sentinel.subnet_id)

        self._neutron._client.show_subnet.assert_called_once_with(
            mock.sentinel.subnet_id)
        self.assertEqual(self._FAKE_CIDR, cidr)
        self.assertEqual(self._FAKE_GATEWAY, gw)

    def test_get_network_subnet_cidr_exception(self):
        self._neutron._client.show_subnet.side_effect = Exception("Fail")
        cidr, gw = self._neutron.get_network_subnet_cidr_and_gateway(
            mock.sentinel.subnet_id)
        self.assertIsNone(cidr)
        self.assertIsNone(gw)

    def test_get_port_ip_address(self):
        self._neutron._client.show_port.return_value = {
            'port': {
                'fixed_ips': [{'ip_address': mock.sentinel.ip_addr}]
            }
        }

        ip_addr = self._neutron.get_port_ip_address(mock.sentinel.fake_port_id)

        self._neutron._client.show_port.assert_called_once_with(
            mock.sentinel.fake_port_id)
        self.assertEqual(mock.sentinel.ip_addr, ip_addr)

    def test_get_port_ip_address_exception(self):
        self._neutron._client.show_port.side_effect = Exception("Fail")
        ip_addr = self._neutron.get_port_ip_address(mock.sentinel.fake_port_id)
        self.assertIsNone(ip_addr)

    def test_get_tunneling_agents(self):
        non_tunnel_agent = {}
        ignored_agent = {'configurations': {
            'tunnel_types': [constants.TYPE_NVGRE]}
        }
        tunneling_agent = {
            'configurations': {'tunnel_types': [constants.TYPE_NVGRE],
                               'tunneling_ip': mock.sentinel.tunneling_ip},
            'host': self._FAKE_HOST
        }

        self._neutron._client.list_agents.return_value = {
            'agents': [non_tunnel_agent, ignored_agent, tunneling_agent]
        }

        actual = self._neutron.get_tunneling_agents()
        self.assertEqual({self._FAKE_HOST: mock.sentinel.tunneling_ip}, actual)

    def test_get_tunneling_agents_exception(self):
        self._neutron._client.list_agents.side_effect = Exception("Fail")
        actual = self._neutron.get_tunneling_agents()
        self.assertEqual({}, actual)

    def test_get_network_ports(self):
        self._neutron._client.list_ports.return_value = {
            'ports': [mock.sentinel.port]
        }

        actual = self._neutron.get_network_ports(key='value')

        self._neutron._client.list_ports.assert_called_once_with(key='value')
        self.assertEqual([mock.sentinel.port], actual)

    def test_get_network_ports_exception(self):
        self._neutron._client.list_ports.side_effect = Exception("Fail")
        actual = self._neutron.get_network_ports()
        self.assertEqual([], actual)
