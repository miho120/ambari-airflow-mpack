#!/usr/bin/env python
import os,re
import resource_management.libraries.functions
from resource_management import *
from ambari_commons.os_check import OSCheck
from ambari_commons.str_utils import cbool, cint
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.get_stack_version import get_stack_version
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.script.script import Script
import functools
# a map of the Ambari role to the component name
# for use with <stack-root>/current/<component>
SERVER_ROLE_DIRECTORY_MAP = {
  'AIRFLOW_WEBSERVER' : 'airflow-webserver',
  'AIRFLOW_SCHEDULER' : 'airflow-scheduler',
  'AIRFLOW_WORKER' : 'airflow-worker'
}

component_directory_web = Script.get_component_from_role(SERVER_ROLE_DIRECTORY_MAP, "AIRFLOW_WEBSERVER")
component_directory_sched = Script.get_component_from_role(SERVER_ROLE_DIRECTORY_MAP, "AIRFLOW_SCHEDULER")
component_directory_work = Script.get_component_from_role(SERVER_ROLE_DIRECTORY_MAP, "AIRFLOW_WORKER")
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root = Script.get_stack_root()
# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)
stack_name = default("/hostLevelParams/stack_name", None)
#e.g. /var/lib/ambari-agent/cache/stacks/HDP/$VERSION/services/AIRFLOW/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
cluster_name = str(config['clusterName'])
ambari_server_hostname = config['clusterHostInfo']['ambari_server_host'][0]

airflow_home = config['configurations']['airflow-core-site']['airflow_home']
airflow_user = config['configurations']['airflow-env']['airflow_user']
airflow_group = config['configurations']['airflow-env']['airflow_group']
airflow_webserver_pid_file = config['configurations']['airflow-env']['airflow_webserver_pid_file']
airflow_scheduler_pid_file = config['configurations']['airflow-env']['airflow_scheduler_pid_file']
airflow_worker_pid_file = config['configurations']['airflow-env']['airflow_worker_pid_file']
airflow_pip_params = config['configurations']['airflow-env']['airflow_pip_params']
