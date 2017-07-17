* politraf
  * systat.py - system statistic to clickhouse
  * connstat.py - connections statistic to clickhouse
  * constat.service and systat.service - config for systemd
  * politraf_clickhouse.json - grafana dashboard (Grafana 4.4)
  * config.yaml - configuration file
* install
  * apt-get install tshark
  * pip install infi.clickhouse_orm
  * pip install pyshark
  * pip install pyyaml
  * mkdir /etc/politraf
  * cp config.yaml /etc/politraf/
  * mkdir /usr/local/bin/politraf
  * cp systat.py constat.py /usr/local/bin/politraf
  * chmod +x /usr/local/bin/politraf/systat.py /usr/local/bin/politraf/constat.py
  * cp constat.service systat.service /etc/systemd/system/
* services
  * service systat (start|stop|status)
  * service constat (start|stop|status)
* clickhouse - https://clickhouse.yandex/docs/en/getting_started/index.html#installation
* grafana - http://docs.grafana.org/installation/