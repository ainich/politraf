[![Build Status](https://travis-ci.org/ainich/politraf.svg?branch=master)](https://travis-ci.org/ainich/politraf) [![GitHub release](https://img.shields.io/github/release/ainich/politraf.svg)](https://github.com/ainich/politraf/issues) [![GitHub issues](https://img.shields.io/github/issues/ainich/politraf.svg)](https://github.com/ainich/politraf/issues)

![Politraf](https://politraf.ru/static/img/politraf.jpg)

* Install (Ubuntu 14.04 - trusty OR Ubuntu 16.04  xenial OR Debian 8 - jessie, Python 3, **CPU with SSE 4.2**)

    * Clickhouse

      Ubuntu | Debian | action
      ------------ | ------------- | -------------
      16.04  xenial | 9 stretch | Add to /etc/apt/sources.list - deb http://repo.yandex.ru/clickhouse/xenial stable main
      14.04  trusty | 8 jessie | Add to /etc/apt/sources.list - deb http://repo.yandex.ru/clickhouse/trusty stable main
      
      ```
      sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
      sudo apt-get update
      sudo apt-get install clickhouse-client clickhouse-server-common
      ```

  
    * Grafana
      * Add to /etc/apt/sources.list - "deb https://packagecloud.io/grafana/stable/debian/ jessie main"

      ```
      curl https://packagecloud.io/gpg.key | sudo apt-key add -
      sudo apt-get update
      sudo apt-get install grafana
      grafana-cli plugins install vertamedia-clickhouse-datasource
      ```

      * Add datasource named Clickhouse
      * Add dashboard from https://grafana.com/dashboards/2996

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
    sudo vi /etc/politraf/config.yaml
    sudo systemctl daemon-reload
    sudo systemctl start systat
    sudo systemctl start constat

    crontab -e
    0 2 * * * /opt/politraf/otxget.py >/dev/null 2>&1
    */2 * * * * /opt/politraf/iocwatch.py >/dev/null 2>&1
    ```