# Apache Airflow management pack for Apache Ambari (airflow-ambari-mpack)

[![Mpack version](https://img.shields.io/badge/Mpack%20version-1.5.4-brightgreen.svg)](https://github.com/miho120/ambari-airflow-mpack)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)

Mpack allows you to install/configure airflow directly from ambari.
Apache Airflow version included: 1.10.0

#### Installing Apache Aiflow Mpack:
1. Stop Ambari server.
2. Install the Apache Airflow Mpack on Ambari server.
3. Start Ambari server.

```
ambari-server stop
ambari-server install-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server start
```

#### Upgrading Apache Aiflow Mpack:
1. Stop Ambari server.
2. Upgrade the Apache Airflow Mpack on Ambari server.
3. Start Ambari server.

```
ambari-server stop
ambari-server upgrade-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server start
```

### Installing Apache Airflow from Ambari:
1. Action - Add service.
2. Select Apache Airflow service.
3. Choose destination server.
4. You may configure Apache Airflow, change home folder.
5. Deploy!

![Add service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/1.PNG)
![Select Apache Airflow service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/2.PNG)
![Choose destination server](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/3.PNG)
![Choose destination server](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/3-1.PNG)
![configure Apache Airflow](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/4.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/5.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/6.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/8.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/10.PNG)

### Virtual environment support
If you want to run apache airflow in virtual environment, you should modify startup script "AIRFLOW_HOME/airflow_control.sh".

Example:
```
#!/bin/bash

export AIRFLOW_HOME=/usr/local/airflow/airflow/ && source /usr/local/airflow/airflow_venv/airflow/bin/activate && /usr/local/airflow/airflow_venv/airflow/bin/airflow $1 --pid /usr/local/airflow/airflow/airflow-sys-$1.pid
```

### Enjoy!
