![Politraf](https://politraf.ru/static/img/politraf.jpg)

* Politraf
  * systat.py - system statistic to clickhouse
  * connstat.py - connections statistic to clickhouse
  * otxget.py - Fetch IOC pulse from OTX AlienVault
  * iocwatch.py - Check traffic for IOC and report
  * constat.service and systat.service - config for systemd
  * politraf_clickhouse.json - grafana dashboard (Grafana 4.4)
  * config.yaml - configuration file (interface, capture filter - https://wiki.wireshark.org/CaptureFilters)
  * Services
    * service systat (start|stop|status)
    * service constat (start|stop|status)

* Install (Debian, **Python 3 required**)
  ```
  sudo apt-get install tshark
  pip3 install infi.clickhouse_orm
  pip3 install pyshark
  pip3 install pyyaml
  mkdir /etc/politraf
  cp config.yaml /etc/politraf/
  mkdir /opt/politraf
  cp systat.py constat.py otxget.py /opt/politraf
  cp constat.service systat.service /etc/systemd/system/
  ```
  crontab -e
    * add line - 0 2 * * * /opt/politraf/otxget.py
    * add line - */5 * * * * /opt/politraf/iocwatch.py

* Clickhouse - https://clickhouse.yandex/docs/en/getting_started/index.html#installation
  
  Ubuntu | Debian
  ------------ | -------------
  16.04  xenial | stretch / sid
  14.04  trusty | jessie  / sid
  
* Grafana - http://docs.grafana.org/installation/
  * Install Clickhouse datasource for Grafana - https://grafana.com/plugins/vertamedia-clickhouse-datasource
  * Add datasource named Clickhouse

* OTX AlienVault - https://otx.alienvault.com
  * Create an account and select your feeds
  * Set API key in /etc/politraf.cfg