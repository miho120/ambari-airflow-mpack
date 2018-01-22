# airflow-ambari-mpack

Airflow mpack for ambari.
Mpack allows you to install/configure airflow directly from ambari.
Airflow installation from this Mpack doesn't require internet connection on your server.

Airflow version included: 1.9.0

#### Installing Aiflow Mpack:
1. Stop Ambari server.
2. Deploy the Example MPack on Ambari server.
3. Start Ambari server.

```
ambari-server install-mpack --mpack=airflow-service-mpack.tar.gz
ambari-server stop
ambari-server start
```

### Installing Airflow from Ambari:
1. Action - Add service.
2. Select Airflow service.
3. Choose destination server.
4. You may configure Airflow, change installation folder.
5. Deploy!

![Add service](/screeshots/1.PNG)
![Select Airflow service](/screeshots/2.PNG)
![Choose destination server](/screeshots/3.PNG)
![configure Airflow](/screeshots/4.PNG)
![Deploy](/screeshots/5.PNG)
![Deploy](/screeshots/6.PNG)
![Deploy](/screeshots/7.PNG)
![Deploy](/screeshots/8.PNG)
![Deploy](/screeshots/9.PNG)
