[![Build Status](https://travis-ci.org/ainich/politraf.svg?branch=master)](https://travis-ci.org/ainich/politraf)

![Politraf](https://politraf.ru/static/img/politraf.jpg)

* Politraf
  * systat.py - system statistic to clickhouse
  * connstat.py - connections statistic to clickhouse
  * otxget.py - Fetch IOC pulse from OTX AlienVault
  * iocwatch.py - Check traffic for IOC and report
  * dbmodels.py - ORM clickhouse
  * config
    * constat.service and systat.service - config for systemd
    * politraf_clickhouse.json - grafana dashboard (Grafana 4.4)
    * config.yaml - configuration file (interface, capture filter - https://wiki.wireshark.org/CaptureFilters, etc)
  * Services
    * service systat (start|stop|status)
    * service constat (start|stop|status)

* Install (Ubuntu, Python 3, CPU with SSE 4.2)

    * Clickhouse - https://clickhouse.yandex/docs/en/getting_started/index.html#installation
  
      Ubuntu | Debian
      ------------ | -------------
      16.04  xenial | stretch / sid
      14.04  trusty | jessie  / sid
  
    * Grafana - http://docs.grafana.org/installation/
      * Install Clickhouse datasource for Grafana - https://grafana.com/plugins/vertamedia-clickhouse-datasource
      * Add datasource named Clickhouse
      * Add dashboard from /config/politraf_clickhouse.json - http://docs.grafana.org/reference/export_import/

    * OTX AlienVault - https://otx.alienvault.com
      * Create an account and select your feeds
      * Set API key in /etc/politraf.cfg


    ```
    git clone https://github.com/ainich/politraf.git
    sudo apt-get install tshark
    sudo apt-get install python3-pip
    cd politraf
    sudo pip3 install -r requirements.txt
    sudo ./setup.py
    vim /etc/politraf/config.yaml
    sudo systemctl daemon-reload
    sudo systemctl start systat
    sudo systemctl start constat

    crontab -e
    0 2 * * * /opt/politraf/otxget.py >/dev/null 2>&1
    */2 * * * * /opt/politraf/iocwatch.py >/dev/null 2>&1
    ```