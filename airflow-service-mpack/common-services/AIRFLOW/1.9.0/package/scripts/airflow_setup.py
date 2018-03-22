#!/usr/bin/env python
import sys, os, pwd, grp, signal, time, base64
from resource_management import *
from resource_management.core.exceptions import Fail
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, Directory, File
from resource_management.core.shell import call
from resource_management.core.system import System
from resource_management.libraries.functions.default import default

def airflow_make_systemd_scripts_webserver(env):
	import params
	env.set_params(params)

	confFileText = format("""[Unit]
Description=Airflow webserver daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service

[Service]
EnvironmentFile=/etc/sysconfig/airflow
User={airflow_user}
Group={airflow_group}
Type=simple
ExecStart={airflow_home}/airflow_control.sh webserver
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

""")

	with open("/etc/systemd/system/multi-user.target.wants/airflow-webserver.service", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	confFileText = format("AIRFLOW_HOME={airflow_home}")

	with open("/etc/sysconfig/airflow", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	Execute("systemctl daemon-reload")

def airflow_make_systemd_scripts_scheduler(env):
	import params
	env.set_params(params)

	confFileText = format("""[Unit]
Description=Airflow scheduler daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service

[Service]
EnvironmentFile=/etc/sysconfig/airflow
User={airflow_user}
Group={airflow_group}
Type=simple
ExecStart={airflow_home}/airflow_control.sh scheduler
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

""")

	with open("/etc/systemd/system/multi-user.target.wants/airflow-scheduler.service", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	confFileText = format("AIRFLOW_HOME={airflow_home}")

	with open("/etc/sysconfig/airflow", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	Execute("systemctl daemon-reload")

def airflow_make_systemd_scripts_worker(env):
	import params
	env.set_params(params)

	confFileText = format("""[Unit]
Description=Airflow worker daemon
After=network.target postgresql.service mysql.service redis.service rabbitmq-server.service
Wants=postgresql.service mysql.service redis.service rabbitmq-server.service

[Service]
EnvironmentFile=/etc/sysconfig/airflow
User={airflow_user}
Group={airflow_group}
Type=simple
ExecStart={airflow_home}/airflow_control.sh worker
Restart=on-failure
RestartSec=5s
PrivateTmp=true

[Install]
WantedBy=multi-user.target

""")

	with open("/etc/systemd/system/multi-user.target.wants/airflow-worker.service", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	confFileText = format("AIRFLOW_HOME={airflow_home}")

	with open("/etc/sysconfig/airflow", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()

	Execute("systemctl daemon-reload")

def airflow_make_startup_script(env):
	import params
	env.set_params(params)

	confFileText = format("""#!/bin/bash

export AIRFLOW_HOME={airflow_home} && /usr/bin/airflow $1 --pid {airflow_home}/airflow-sys-$1.pid
""")

	with open(format("{airflow_home}/airflow_control.sh"), 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()
	Execute(format("chmod 755 {airflow_home}/airflow_control.sh"))

def airflow_configure(env):
	import params
	env.set_params(params)

	confFileText = format("""[core]
airflow_home = {airflow_home}
dags_folder = {dags_folder}
base_log_folder = {base_log_folder}
remote_log_conn_id = {remote_log_conn_id}
encrypt_s3_logs = {encrypt_s3_logs}
logging_level = {logging_level}
logging_config_class = {logging_config_class}
log_format = {log_format}
simple_log_format = {simple_log_format}
executor = {executor}
sql_alchemy_conn = {sql_alchemy_conn}
sql_alchemy_pool_size = {sql_alchemy_pool_size}
sql_alchemy_pool_recycle = {sql_alchemy_pool_recycle}
parallelism = {parallelism}
dag_concurrency = {dag_concurrency}
dags_are_paused_at_creation = {dags_are_paused_at_creation}
non_pooled_task_slot_count = {non_pooled_task_slot_count}
max_active_runs_per_dag = {max_active_runs_per_dag}
load_examples = {load_examples}
plugins_folder = {plugins_folder}
fernet_key = {fernet_key}
donot_pickle = {donot_pickle}
dagbag_import_timeout = {dagbag_import_timeout}
task_runner = {task_runner}
default_impersonation = {default_impersonation}
security = {security}
unit_test_mode = {unit_test_mode}
task_log_reader = {task_log_reader}
enable_xcom_pickling = {enable_xcom_pickling}
killed_task_cleanup_time = {killed_task_cleanup_time}

[cli]
api_client = {api_client}
endpoint_url = {endpoint_url}

[api]
auth_backend = {auth_backend}

[operators]
default_owner = {default_owner}
default_cpus = {default_cpus}
default_ram = {default_ram}
default_disk = {default_disk}
default_gpus = {default_gpus}

[webserver]
base_url = {base_url}
web_server_host = {web_server_host}
web_server_port = {web_server_port}
web_server_ssl_cert = {web_server_ssl_cert}
web_server_ssl_key = {web_server_ssl_key}
web_server_worker_timeout = {web_server_worker_timeout}
worker_refresh_batch_size = {worker_refresh_batch_size}
worker_refresh_interval = {worker_refresh_interval}
secret_key = {secret_key}
workers = {workers}
worker_class = {worker_class}
access_logfile = {access_logfile}
error_logfile = {error_logfile}
expose_config = {expose_config}
authenticate = {authenticate}
filter_by_owner = {filter_by_owner}
owner_mode = {owner_mode}
dag_default_view = {dag_default_view}
dag_orientation = {dag_orientation}
demo_mode = {demo_mode}
log_fetch_timeout_sec = {log_fetch_timeout_sec}
hide_paused_dags_by_default = {hide_paused_dags_by_default}
page_size = {page_size}

[email]
email_backend = {email_backend}

[smtp]
smtp_host = {smtp_host}
smtp_starttls = {smtp_starttls}
smtp_ssl = {smtp_ssl}
smtp_user = {smtp_user}
smtp_password = {smtp_password}
smtp_port = {smtp_port}
smtp_mail_from = {smtp_mail_from}

[celery]
celery_app_name = {celery_app_name}
celeryd_concurrency = {celeryd_concurrency}
worker_log_server_port = {worker_log_server_port}
broker_url = {broker_url}
celery_result_backend = {celery_result_backend}
flower_host = {flower_host}
flower_port = {flower_port}
default_queue = {default_queue}
celery_config_options = {celery_config_options}

[dask]
cluster_address = {cluster_address}

[scheduler]
job_heartbeat_sec = {job_heartbeat_sec}
scheduler_heartbeat_sec = {scheduler_heartbeat_sec}
run_duration = {run_duration}
min_file_process_interval = {min_file_process_interval}
dag_dir_list_interval = {dag_dir_list_interval}
print_stats_interval = {print_stats_interval}
child_process_log_directory = {child_process_log_directory}
scheduler_zombie_task_threshold = {scheduler_zombie_task_threshold}
catchup_by_default = {catchup_by_default}
max_tis_per_query = {max_tis_per_query}
statsd_on = {statsd_on}
statsd_host = {statsd_host}
statsd_port = {statsd_port}
statsd_prefix = {statsd_prefix}
max_threads = {max_threads}
authenticate = {scheduler_authenticate}

[ldap]
uri = {uri}
user_filter = {user_filter}
user_name_attr = {user_name_attr}
group_member_attr = {group_member_attr}
superuser_filter = {superuser_filter}
data_profiler_filter = {data_profiler_filter}
bind_user = {bind_user}
bind_password = {bind_password}
basedn = {basedn}
cacert = {cacert}
search_scope = {search_scope}

[mesos]
master = {mesos_master}
framework_name = {mesos_framework_name}
task_cpu = {mesos_task_cpu}
task_memory = {mesos_task_memory}
checkpoint = {mesos_checkpoint}
failover_timeout = {mesos_failover_timeout}
authenticate = {mesos_authenticate}
default_principal = {mesos_default_principal}
default_secret = {mesos_default_secret}

[kerberos]
ccache = {kerberos_ccache}
principal = {kerberos_principal}
reinit_frequency = {kerberos_reinit_frequency}
kinit_path = {kerberos_kinit_path}
keytab = {kerberos_keytab}

[github_enterprise]
api_rev = {api_rev}

[admin]
hide_sensitive_variable_fields = {hide_sensitive_variable_fields}
""")
	
	with open(params.airflow_home + "/airflow.cfg", 'w') as configFile:
		configFile.write(confFileText)
	configFile.close()
