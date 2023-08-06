# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import mock
from shade.tests.fakes import FakeFlavor, FakeProject

import shade
from keystoneauth1.fixture import keystoneauth_betamax
from keystoneauth1.fixture import serializer
from shade.tests import fakes
from shade.tests.unit import base


class TestFlavorsBetamax(base.BaseTestCase):

    def test_create_flavor(self):
        self.useFixture(keystoneauth_betamax.BetamaxFixture(
            cassette_name='test_create_flavor',
            cassette_library_dir=self.fixtures_directory,
            record=self.record_fixtures,
            serializer=serializer.YamlJsonSerializer))

        old_flavors = self.full_op_cloud.list_flavors()
        self.full_op_cloud.create_flavor(
            'vanilla', 12345, 4, 100
        )

        # test that we have a new flavor added
        new_flavors = self.full_op_cloud.list_flavors()
        self.assertEqual(len(new_flavors) - len(old_flavors), 1)

        # test that new flavor is created correctly
        found = False
        for flavor in new_flavors:
            if flavor['name'] == 'vanilla':
                found = True
                break
        self.assertTrue(found)
        needed_keys = {'name', 'ram', 'vcpus', 'id', 'is_public', 'disk'}
        if found:
            # check flavor content
            self.assertTrue(needed_keys.issubset(flavor.keys()))

        # delete created flavor
        self.full_op_cloud.delete_flavor('vanilla')


class TestFlavors(base.TestCase):

    @mock.patch.object(shade.OpenStackCloud, '_compute_client')
    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_delete_flavor(self, mock_nova, mock_compute):
        mock_response = mock.Mock()
        mock_response.json.return_value = dict(extra_specs=[])
        mock_compute.get.return_value = mock_response
        mock_nova.flavors.list.return_value = [
            fakes.FakeFlavor('123', 'lemon', 100)
        ]
        self.assertTrue(self.op_cloud.delete_flavor('lemon'))
        mock_nova.flavors.delete.assert_called_once_with(flavor='123')

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_delete_flavor_not_found(self, mock_nova):
        mock_nova.flavors.list.return_value = []
        self.assertFalse(self.op_cloud.delete_flavor('invalid'))
        self.assertFalse(mock_nova.flavors.delete.called)

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_delete_flavor_exception(self, mock_nova):
        mock_nova.flavors.list.return_value = [
            fakes.FakeFlavor('123', 'lemon', 100)
        ]
        mock_nova.flavors.delete.side_effect = Exception()
        self.assertRaises(shade.OpenStackCloudException,
                          self.op_cloud.delete_flavor, '')

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_list_flavors(self, mock_nova):
        self.op_cloud.list_flavors()
        mock_nova.flavors.list.assert_called_once_with(is_public=None)

    @mock.patch.object(shade.OpenStackCloud, '_compute_client')
    def test_set_flavor_specs(self, mock_compute):
        extra_specs = dict(key1='value1')
        self.op_cloud.set_flavor_specs(1, extra_specs)
        mock_compute.post.assert_called_once_with(
            '/flavors/{id}/os-extra_specs'.format(id=1),
            json=dict(extra_specs=extra_specs))

    @mock.patch.object(shade.OpenStackCloud, '_compute_client')
    def test_unset_flavor_specs(self, mock_compute):
        keys = ['key1', 'key2']
        self.op_cloud.unset_flavor_specs(1, keys)
        api_spec = '/flavors/{id}/os-extra_specs/{key}'
        self.assertEqual(
            mock_compute.delete.call_args_list[0],
            mock.call(api_spec.format(id=1, key='key1')))
        self.assertEqual(
            mock_compute.delete.call_args_list[1],
            mock.call(api_spec.format(id=1, key='key2')))

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_add_flavor_access(self, mock_nova):
        self.op_cloud.add_flavor_access('flavor_id', 'tenant_id')
        mock_nova.flavor_access.add_tenant_access.assert_called_once_with(
            flavor='flavor_id', tenant='tenant_id'
        )

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_add_flavor_access_by_flavor(self, mock_nova):
        flavor = FakeFlavor(id='flavor_id', name='flavor_name', ram=None)
        tenant = FakeProject('tenant_id')
        self.op_cloud.add_flavor_access(flavor, tenant)
        mock_nova.flavor_access.add_tenant_access.assert_called_once_with(
            flavor=flavor, tenant=tenant
        )

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_remove_flavor_access(self, mock_nova):
        self.op_cloud.remove_flavor_access('flavor_id', 'tenant_id')
        mock_nova.flavor_access.remove_tenant_access.assert_called_once_with(
            flavor='flavor_id', tenant='tenant_id'
        )

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_list_flavor_access(self, mock_nova):
        mock_nova.flavors.list.return_value = [FakeFlavor(
            id='flavor_id', name='flavor_name', ram=None)]
        self.op_cloud.list_flavor_access('flavor_id')
        mock_nova.flavor_access.list.assert_called_once_with(
            flavor='flavor_id'
        )

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    def test_list_flavor_access_by_flavor(self, mock_nova):
        flavor = FakeFlavor(id='flavor_id', name='flavor_name', ram=None)
        self.op_cloud.list_flavor_access(flavor)
        mock_nova.flavor_access.list.assert_called_once_with(
            flavor=flavor
        )
