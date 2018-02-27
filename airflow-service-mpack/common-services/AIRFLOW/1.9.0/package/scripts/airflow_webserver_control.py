import sys, os, pwd, grp, signal, time
from resource_management import *
from subprocess import call
from airflow_setup import *

class AirflowWebserver(Script):
	"""
	Contains the interface definitions for methods like install, 
	start, stop, status, etc. for the Airflow Server
	"""
	def install(self, env):
		import params
		env.set_params(params)
		self.install_packages(env)
		Logger.info(format("Installing Airflow Service"))
		Execute(format("pip install apache-airflow[all]==1.9.0 apache-airflow[celery]==1.9.0"))
		Execute(format("mkdir -p {airflow_home} && chown -R {airflow_user}:{airflow_group} {airflow_home}"))
		Execute(format("export AIRFLOW_HOME={airflow_home} && airflow initdb"),
			user=params.airflow_user
		)

	def configure(self, env):
		import params
		env.set_params(params)
		airflow_configure(env)
		
	def start(self, env):
		import params
		self.configure(env)
		Execute(format("export AIRFLOW_HOME={airflow_home} && airflow webserver &"),
			user=params.airflow_user
		)
		Execute ('ps -ef | grep "airflow webserver" | grep -v grep | awk \'{print $2}\' | tail -n 1 > ' + params.airflow_webserver_pid_file, user=params.airflow_user)

	def stop(self, env):
		import params
		env.set_params(params)
		# Kill the process of Airflow
		Execute ('ps -ef | grep airflow-webserver | grep -v grep | awk	\'{print $2}\' | xargs kill -9', user=params.airflow_user, ignore_failures=True)
		Execute ('ps -ef | grep "airflow webserver" | grep -v grep | awk	\'{print $2}\' | xargs kill -9', user=params.airflow_user, ignore_failures=True)
		File(params.airflow_webserver_pid_file,
			action = "delete",
			owner = params.airflow_user
		)

	def status(self, env):
		import status_params
		env.set_params(status_params)
		#use built-in method to check status using pidfile
		check_process_status(status_params.airflow_webserver_pid_file)

if __name__ == "__main__":
	AirflowWebserver().execute()
