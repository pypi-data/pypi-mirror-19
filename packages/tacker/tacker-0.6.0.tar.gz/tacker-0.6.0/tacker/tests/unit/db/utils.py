# Copyright 2015 Brocade Communications System, Inc.
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

import codecs
import os
import yaml


def _get_template(name):
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../vm/infra_drivers/openstack/data/", name)
    f = codecs.open(filename, encoding='utf-8', errors='strict')
    return f.read()

vnfd_openwrt = _get_template('openwrt.yaml')
tosca_vnfd_openwrt = _get_template('test_tosca_openwrt.yaml')
vnfd_ipparams_template = _get_template('vnf_cirros_template_ipaddr.yaml')
ipparams = _get_template('vnf_cirros_param_values_ipaddr.yaml')
userdata_params = _get_template('vnf_cirros_param_values_user_data.yaml')
config_data = _get_template('config_data.yaml')
update_config_data = _get_template('update_config_data.yaml')
vnffgd_template = yaml.load(_get_template('vnffgd_template.yaml'))
vnffgd_tosca_template = yaml.load(_get_template('tosca_vnffgd_template.yaml'))
vnffgd_invalid_tosca_template = yaml.load(_get_template(
    'tosca_invalid_vnffgd_template.yaml'))
vnfd_scale_tosca_template = _get_template('tosca_scale.yaml')
vnfd_alarm_respawn_tosca_template = _get_template(
    'test_tosca_vnfd_alarm_respawn.yaml')
vnfd_alarm_scale_tosca_template = _get_template(
    'test_tosca_vnfd_alarm_scale.yaml')
nsd_tosca_template = yaml.load(_get_template('tosca_nsd_template.yaml'))


def get_dummy_vnfd_obj():
    return {u'vnfd': {u'service_types': [{u'service_type': u'vnfd'}],
                      'name': 'dummy_vnfd',
                      'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                      u'attributes': {u'vnfd': yaml.safe_load(
                          tosca_vnfd_openwrt)},
                      'description': 'dummy_vnfd_description'},
            u'auth': {u'tenantName': u'admin', u'passwordCredentials': {
                u'username': u'admin', u'password': u'devstack'}}}


def get_dummy_vnf_obj():
    return {'vnf': {'description': 'dummy_vnf_description',
                    'vnfd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
                    'vim_id': u'6261579e-d6f3-49ad-8bc3-a9cb974778ff',
                    'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                    'name': 'dummy_vnf',
                    'attributes': {}}}


def get_dummy_vnf_config_obj():
    return {'vnf': {u'attributes': {u'config': {'vdus': {'vdu1': {
        'config': {'firewall': 'dummy_firewall_values'}}}}}}}


def get_dummy_device_obj():
    return {'status': 'PENDING_CREATE', 'instance_id': None, 'name':
        u'test_openwrt', 'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
        'vnfd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
        'vnfd': {
            'service_types': [{'service_type': u'vnfd',
            'id': u'4a4c2d44-8a52-4895-9a75-9d1c76c3e738'}],
            'description': u'OpenWRT with services',
            'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
            'mgmt_driver': u'openwrt',
            'attributes': {u'vnfd': vnfd_openwrt},
            'id': u'fb048660-dc1b-4f0f-bd89-b023666650ec',
            'name': u'openwrt_services'},
        'mgmt_url': None, 'service_context': [],
        'attributes': {u'param_values': u''},
        'id': 'eb84260e-5ff7-4332-b032-50a14d6c1123',
        'description': u'OpenWRT with services'}


def get_dummy_vnf_config_attr():
    return {'status': 'PENDING_CREATE', 'instance_id': None, 'name':
        u'test_openwrt', 'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
        'vnfd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
        'vnfd': {'service_types': [{'service_type': u'vnfd',
            'id': u'4a4c2d44-8a52-4895-9a75-9d1c76c3e738'}],
            'description': u'OpenWRT with services',
            'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
            'mgmt_driver': u'openwrt',
            'attributes': {u'vnfd': tosca_vnfd_openwrt},
            'id': u'fb048660-dc1b-4f0f-bd89-b023666650ec', 'name':
            u'openwrt_services'}, 'mgmt_url': None, 'service_context': [],
            'attributes': {u'config': config_data},
            'id': 'eb84260e-5ff7-4332-b032-50a14d6c1123',
            'description': u'OpenWRT with services'}


def get_dummy_vnf_update_config():
    return {'vnf': {'attributes': {'config': update_config_data}}}


def get_dummy_device_obj_ipaddr_attr():
    return {'status': 'PENDING_CREATE',
        'vnfd': {'service_types':
            [{'service_type': u'vnfd', 'id':
                u'16f8b3f7-a9ff-4338-bbe5-eee48692c468'}, {'service_type':
                u'router', 'id': u'58878cb7-689f-47a5-9c2d-654e49e2357f'},
             {'service_type': u'firewall', 'id':
                 u'd016144f-42a6-44f4-93f6-52d201998916'}],
            'description': u'Parameterized VNF descriptor for IP addresses',
            'tenant_id': u'4dd6c1d7b6c94af980ca886495bcfed0',
            'mgmt_driver': u'noop',
            'attributes': {u'vnfd': vnfd_ipparams_template},
            'id': u'24c31ea1-2e28-4de2-a6cb-8d389a502c75', 'name': u'ip_vnfd'},
        'name': u'test_ip',
        'tenant_id': u'8273659b56fc46b68bd05856d1f08d14',
        'id': 'd1337add-d5a1-4fd4-9447-bb9243c8460b',
        'instance_id': None, 'mgmt_url': None, 'service_context': [],
        'services': [],
        'attributes': {u'param_values': ipparams},
        'vnfd_id': u'24c31ea1-2e28-4de2-a6cb-8d389a502c75',
        'description': u'Parameterized VNF descriptor for IP addresses'}


def get_vim_obj():
    return {'vim': {'type': 'openstack', 'auth_url':
                    'http://localhost:5000', 'vim_project': {'name':
                    'test_project'}, 'auth_cred': {'username': 'test_user',
                                                   'password':
                                                       'test_password'},
                            'name': 'VIM0',
                    'tenant_id': 'test-project'}}


def get_vim_auth_obj():
    return {'username': 'test_user',
            'password': 'test_password',
            'project_id': None,
            'project_name': 'test_project',
            'auth_url': 'http://localhost:5000/v3',
            'user_domain_name': 'default',
            'project_domain_name': 'default'}


def get_dummy_vnffgd_obj():
    return {u'vnffgd': {'name': 'dummy_vnfd',
                        'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                        u'template': {u'vnffgd': vnffgd_tosca_template},
                        'description': 'dummy_vnfd_description'}}


def get_dummy_vnffg_obj():
    return {'vnffg': {'description': 'dummy_vnf_description',
                      'vnffgd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
                      'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                      'name': 'dummy_vnffg',
                      'vnf_mapping': {},
                      'symmetrical': False}}


def get_dummy_vnffg_obj_vnf_mapping():
    return {'vnffg': {'description': 'dummy_vnf_description',
                      'vnffgd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
                      'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                      'name': 'dummy_vnffg',
                      'vnf_mapping': {
                          'VNF1': '91e32c20-6d1f-47a4-9ba7-08f5e5effe07',
                          'VNF3': '7168062e-9fa1-4203-8cb7-f5c99ff3ee1b'
                      },
                      'symmetrical': False}}


def get_dummy_nsd_obj():
    return {'nsd': {'description': 'dummy nsd description',
                    'name': 'dummy_NSD',
                    'tenant_id': u'8819a1542a5948b68f94d4be0fd50496',
                    'template': {},
                    'attributes': {u'nsd': nsd_tosca_template}}}


def get_dummy_ns_obj():
    return {'ns': {'description': 'dummy_ns_description',
                   'id': u'ba6bf017-f6f7-45f1-a280-57b073bf78ea',
                   'nsd_id': u'eb094833-995e-49f0-a047-dfb56aaf7c4e',
                   'vim_id': u'6261579e-d6f3-49ad-8bc3-a9cb974778ff',
                   'tenant_id': u'ad7ebc56538745a08ef7c5e97f8bd437',
                   'name': 'dummy_ns',
                   'attributes': {
                       'param_values': {'nsd': {'vl1_name': 'net_mgmt',
                                                'vl2_name': 'net0'}}}}}
