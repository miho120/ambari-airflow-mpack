# airflow-ambari-mpack

Airflow version included: 1.9.0

Using the Aiflow MPack
Stop Ambari server:

ambari-server stop

Deploy the Example MPack on Ambari server:

ambari-server install-mpack --mpack=airflow-service-mpack.tar.gz

Start Ambari server:

ambari-server start
