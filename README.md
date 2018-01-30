# airflow-ambari-mpack

Apache Airflow mpack for ambari.
Mpack allows you to install/configure airflow directly from ambari.
Apache Airflow installation from this Mpack doesn't require internet connection on your server.

Apache Airflow version included: 1.9.0

#### Installing Apache Aiflow Mpack:
1. Stop Ambari server.
2. Install the Apache Airflow Mpack on Ambari server.
3. Start Ambari server.

```
ambari-server stop
ambari-server install-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server start
```

### Installing ApacheAirflow from Ambari:
1. Action - Add service.
2. Select Apache Airflow service.
3. Choose destination server.
4. You may configure Apache Airflow, change installation folder.
5. Deploy!

![Add service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/1.PNG)
![Select Apache Airflow service](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/2.PNG)
![Choose destination server](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/3.PNG)
![configure Apache Airflow](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/4.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/5.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/6.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/7.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/8.PNG)
![Deploy](https://github.com/miho120/ambari-airflow-mpack/blob/master/Screenshots/9.PNG)


### Enjoy!
