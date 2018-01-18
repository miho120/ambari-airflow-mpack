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
  'AIRFLOW_SERVER' : 'airflow-server',
}

component_directory = Script.get_component_from_role(SERVER_ROLE_DIRECTORY_MAP, "AIRFLOW_SERVER")
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

airflow_install_dir = config['configurations']['airflow-env']['airflow_install_dir']
airflow_user = config['configurations']['airflow-env']['airflow_user']
airflow_group = config['configurations']['airflow-env']['airflow_group']
airflow_pid_file = config['configurations']['airflow-env']['airflow_pid_file']

#[core]
airflow_home = config['configurations']['airflow-core-site']['airflow_home']
dags_folder = config['configurations']['airflow-core-site']['dags_folder']
base_log_folder = config['configurations']['airflow-core-site']['base_log_folder']
remote_log_conn_id = config['configurations']['airflow-core-site']['remote_log_conn_id']
encrypt_s3_logs = config['configurations']['airflow-core-site']['encrypt_s3_logs']
logging_level = config['configurations']['airflow-core-site']['logging_level']
logging_config_class = config['configurations']['airflow-core-site']['logging_config_class']
log_format = config['configurations']['airflow-core-site']['log_format']
simple_log_format = config['configurations']['airflow-core-site']['simple_log_format']
executor = config['configurations']['airflow-core-site']['executor']
sql_alchemy_conn = config['configurations']['airflow-core-site']['sql_alchemy_conn']
sql_alchemy_pool_size = config['configurations']['airflow-core-site']['sql_alchemy_pool_size']
sql_alchemy_pool_recycle = config['configurations']['airflow-core-site']['sql_alchemy_pool_recycle']
parallelism = config['configurations']['airflow-core-site']['parallelism']
dag_concurrency = config['configurations']['airflow-core-site']['dag_concurrency']
dags_are_paused_at_creation = config['configurations']['airflow-core-site']['dags_are_paused_at_creation']
non_pooled_task_slot_count = config['configurations']['airflow-core-site']['non_pooled_task_slot_count']
max_active_runs_per_dag = config['configurations']['airflow-core-site']['max_active_runs_per_dag']
load_examples = config['configurations']['airflow-core-site']['load_examples']
plugins_folder = config['configurations']['airflow-core-site']['plugins_folder']
fernet_key = config['configurations']['airflow-core-site']['fernet_key']
donot_pickle = config['configurations']['airflow-core-site']['donot_pickle']
dagbag_import_timeout = config['configurations']['airflow-core-site']['dagbag_import_timeout']
task_runner = config['configurations']['airflow-core-site']['task_runner']
default_impersonation = config['configurations']['airflow-core-site']['default_impersonation']
security = config['configurations']['airflow-core-site']['security']
unit_test_mode = config['configurations']['airflow-core-site']['unit_test_mode']
task_log_reader = config['configurations']['airflow-core-site']['task_log_reader']
enable_xcom_pickling = config['configurations']['airflow-core-site']['enable_xcom_pickling']
killed_task_cleanup_time = config['configurations']['airflow-core-site']['killed_task_cleanup_time']

# [cli]
api_client = config['configurations']['airflow-cli-site']['api_client']
endpoint_url = config['configurations']['airflow-cli-site']['endpoint_url']

# [api]
auth_backend = config['configurations']['airflow-api-site']['auth_backend']

# [operators]
default_owner = config['configurations']['airflow-operators-site']['default_owner']
default_cpus = config['configurations']['airflow-operators-site']['default_cpus']
default_ram = config['configurations']['airflow-operators-site']['default_ram']
default_disk = config['configurations']['airflow-operators-site']['default_disk']
default_gpus = config['configurations']['airflow-operators-site']['default_gpus']

# [webserver]
base_url = config['configurations']['airflow-webserver-site']['base_url']
web_server_host = config['configurations']['airflow-webserver-site']['web_server_host']
web_server_port = config['configurations']['airflow-webserver-site']['web_server_port']
web_server_ssl_cert = config['configurations']['airflow-webserver-site']['web_server_ssl_cert']
web_server_ssl_key = config['configurations']['airflow-webserver-site']['web_server_ssl_key']
web_server_worker_timeout = config['configurations']['airflow-webserver-site']['web_server_worker_timeout']
worker_refresh_batch_size = config['configurations']['airflow-webserver-site']['worker_refresh_batch_size']
worker_refresh_interval = config['configurations']['airflow-webserver-site']['worker_refresh_interval']
secret_key = config['configurations']['airflow-webserver-site']['secret_key']
workers = config['configurations']['airflow-webserver-site']['workers']
worker_class = config['configurations']['airflow-webserver-site']['worker_class']
access_logfile = config['configurations']['airflow-webserver-site']['access_logfile']
error_logfile = config['configurations']['airflow-webserver-site']['error_logfile']
expose_config = config['configurations']['airflow-webserver-site']['expose_config']
authenticate = config['configurations']['airflow-webserver-site']['authenticate']
filter_by_owner = config['configurations']['airflow-webserver-site']['filter_by_owner']
owner_mode = config['configurations']['airflow-webserver-site']['owner_mode']
dag_default_view = config['configurations']['airflow-webserver-site']['dag_default_view']
dag_orientation = config['configurations']['airflow-webserver-site']['dag_orientation']
demo_mode = config['configurations']['airflow-webserver-site']['demo_mode']
log_fetch_timeout_sec = config['configurations']['airflow-webserver-site']['log_fetch_timeout_sec']
hide_paused_dags_by_default = config['configurations']['airflow-webserver-site']['hide_paused_dags_by_default']
page_size = config['configurations']['airflow-webserver-site']['page_size']

# [email]
email_backend = config['configurations']['airflow-email-site']['email_backend']

# [smtp]
smtp_host = config['configurations']['airflow-smtp-site']['smtp_host']
smtp_starttls = config['configurations']['airflow-smtp-site']['smtp_starttls']
smtp_ssl = config['configurations']['airflow-smtp-site']['smtp_ssl']
smtp_user = config['configurations']['airflow-smtp-site']['smtp_user']
smtp_password = config['configurations']['airflow-smtp-site']['smtp_password']
smtp_port = config['configurations']['airflow-smtp-site']['smtp_port']
smtp_mail_from = config['configurations']['airflow-smtp-site']['smtp_mail_from']


# [celery]
celery_app_name = config['configurations']['airflow-celery-site']['celery_app_name']
celeryd_concurrency = config['configurations']['airflow-celery-site']['celeryd_concurrency']
worker_log_server_port = config['configurations']['airflow-celery-site']['worker_log_server_port']
broker_url = config['configurations']['airflow-celery-site']['broker_url']
celery_result_backend = config['configurations']['airflow-celery-site']['celery_result_backend']
flower_host = config['configurations']['airflow-celery-site']['flower_host']
flower_port = config['configurations']['airflow-celery-site']['flower_port']
default_queue = config['configurations']['airflow-celery-site']['default_queue']
celery_config_options = config['configurations']['airflow-celery-site']['celery_config_options']

# [dask]
cluster_address = config['configurations']['airflow-dask-site']['cluster_address']

# [scheduler]
job_heartbeat_sec = config['configurations']['airflow-scheduler-site']['job_heartbeat_sec']
scheduler_heartbeat_sec = config['configurations']['airflow-scheduler-site']['scheduler_heartbeat_sec']
run_duration = config['configurations']['airflow-scheduler-site']['run_duration']
min_file_process_interval = config['configurations']['airflow-scheduler-site']['min_file_process_interval']
dag_dir_list_interval = config['configurations']['airflow-scheduler-site']['dag_dir_list_interval']
print_stats_interval = config['configurations']['airflow-scheduler-site']['print_stats_interval']
child_process_log_directory = config['configurations']['airflow-scheduler-site']['child_process_log_directory']
scheduler_zombie_task_threshold = config['configurations']['airflow-scheduler-site']['scheduler_zombie_task_threshold']
catchup_by_default = config['configurations']['airflow-scheduler-site']['catchup_by_default']
max_tis_per_query = config['configurations']['airflow-scheduler-site']['max_tis_per_query']
statsd_on = config['configurations']['airflow-scheduler-site']['statsd_on']
statsd_host = config['configurations']['airflow-scheduler-site']['statsd_host']
statsd_port = config['configurations']['airflow-scheduler-site']['statsd_port']
statsd_prefix = config['configurations']['airflow-scheduler-site']['statsd_prefix']
max_threads = config['configurations']['airflow-scheduler-site']['max_threads']
scheduler_authenticate = config['configurations']['airflow-scheduler-site']['scheduler_authenticate']

# [ldap]
uri = config['configurations']['airflow-ldap-site']['uri']
user_filter = config['configurations']['airflow-ldap-site']['user_filter']
user_name_attr = config['configurations']['airflow-ldap-site']['user_name_attr']
group_member_attr = config['configurations']['airflow-ldap-site']['group_member_attr']
superuser_filter = config['configurations']['airflow-ldap-site']['superuser_filter']
data_profiler_filter = config['configurations']['airflow-ldap-site']['data_profiler_filter']
bind_user = config['configurations']['airflow-ldap-site']['bind_user']
bind_password = config['configurations']['airflow-ldap-site']['bind_password']
basedn = config['configurations']['airflow-ldap-site']['basedn']
cacert = config['configurations']['airflow-ldap-site']['cacert']
search_scope = config['configurations']['airflow-ldap-site']['search_scope']

# [mesos]
mesos_master = config['configurations']['airflow-mesos-site']['mesos_master']
mesos_framework_name = config['configurations']['airflow-mesos-site']['mesos_framework_name']
mesos_task_cpu = config['configurations']['airflow-mesos-site']['mesos_task_cpu']
mesos_task_memory = config['configurations']['airflow-mesos-site']['mesos_task_memory']
mesos_checkpoint = config['configurations']['airflow-mesos-site']['mesos_checkpoint']
mesos_failover_timeout = config['configurations']['airflow-mesos-site']['mesos_failover_timeout']
mesos_authenticate = config['configurations']['airflow-mesos-site']['mesos_authenticate']
mesos_default_principal = config['configurations']['airflow-mesos-site']['mesos_default_principal']
mesos_default_secret = config['configurations']['airflow-mesos-site']['mesos_default_secret']

# [kerberos]
kerberos_ccache = config['configurations']['airflow-kerberos-site']['kerberos_ccache']
kerberos_principal = config['configurations']['airflow-kerberos-site']['kerberos_principal']
kerberos_reinit_frequency = config['configurations']['airflow-kerberos-site']['kerberos_reinit_frequency']
kerberos_kinit_path = config['configurations']['airflow-kerberos-site']['kerberos_kinit_path']
kerberos_keytab = config['configurations']['airflow-kerberos-site']['kerberos_keytab']

# [github_enterprise]
api_rev = config['configurations']['airflow-githubenterprise-site']['api_rev']

# [admin]
hide_sensitive_variable_fields = config['configurations']['airflow-admin-site']['hide_sensitive_variable_fields']
