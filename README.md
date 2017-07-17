* politraf
  * systat.py - system statistic to clickhouse
  * connstat.py - connections statistic to clickhouse
  * constat.service and systat.service - config for systemd
  * politraf_clickhouse.json - grafana dashboard (Grafana 4.4)
  * config.yaml - configuration file (interface, capture filter - https://wiki.wireshark.org/CaptureFilters)
* install (Debian, **Python 3 required**)
  ```
  apt-get install tshark
  pip install infi.clickhouse_orm
  pip install pyshark
  pip install pyyaml
  mkdir /etc/politraf
  cp config.yaml /etc/politraf/
  mkdir /usr/local/bin/politraf
  cp systat.py constat.py /usr/local/bin/politraf
  chmod +x /usr/local/bin/politraf/systat.py /usr/local/bin/politraf/constat.py
  cp constat.service systat.service /etc/systemd/system/
  ```
* services
  * service systat (start|stop|status)
  * service constat (start|stop|status)
* clickhouse - https://clickhouse.yandex/docs/en/getting_started/index.html#installation
  
  Ubuntu | Debian
  ------------ | -------------
  17.04  zesty | stretch / sid
  16.10  yakkety | stretch / sid
  16.04  xenial | stretch / sid
  15.10  wily | jessie  / sid
  15.04  vivid | jessie  / sid
  14.10  utopic | jessie  / sid
  14.04  trusty | jessie  / sid
  13.10  saucy | wheezy  / sid
  13.04  raring | wheezy  / sid
  12.10  quantal | wheezy  / sid
  12.04  precise | wheezy  / sid
  11.10  oneiric | wheezy  / sid
  11.04  natty | squeeze / sid
  10.10  maverick | squeeze / sid
  10.04  lucid | squeeze / sid
* grafana - http://docs.grafana.org/installation/