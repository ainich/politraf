[![Build Status](https://travis-ci.org/ainich/politraf.svg?branch=master)](https://travis-ci.org/ainich/politraf)
[![Updates](https://pyup.io/repos/github/ainich/politraf/shield.svg)](https://pyup.io/repos/github/ainich/politraf/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1f170d9dc59343daacae8bdb505468c2)](https://www.codacy.com/app/ainich/politraf?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ainich/politraf&amp;utm_campaign=Badge_Grade)


![Politraf](https://raw.githubusercontent.com/ainich/politraf/master/politraf.jpg)

* Install (Ubuntu 14.04 - trusty OR Ubuntu 16.04  xenial OR Debian 8 - jessie, **Python 3, CPU with SSE 4.2**)

    * Clickhouse

      * Add repository
          * Ubuntu 16.04 Xenial
          ```
          echo 'deb http://repo.yandex.ru/clickhouse/xenial stable main' | sudo tee -a /etc/apt/sources.list
          ```
          * Ubuntu 14.04  Trusty 
          ```
          echo 'deb http://repo.yandex.ru/clickhouse/trusty' | sudo tee -a /etc/apt/sources.list
          ```
      ```
      sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4
      sudo apt-get update
      sudo apt-get install clickhouse-client clickhouse-server-common
      sudo service clickhouse-server start
      ```

  
    * Grafana
      * Add to /etc/apt/sources.list - "deb https://packagecloud.io/grafana/stable/debian/ jessie main"

      ```
      curl https://packagecloud.io/gpg.key | sudo apt-key add -
      sudo apt-get update
      sudo apt-get install grafana
      sudo grafana-cli plugins install vertamedia-clickhouse-datasource
      sudo service grafana-server restart
      ```
      
      * http on port 3000
      * Add datasource named Clickhouse
      * Add dashboard from https://grafana.com/dashboards/2996
      * Add dashboard from https://grafana.com/dashboards/3248

    ```
    git clone https://github.com/ainich/politraf.git
    sudo apt-get install tshark
    sudo apt-get install python3-pip
    cd politraf
    export LC_ALL=C
    sudo pip3 install -r requirements.txt
    sudo pip3 install --upgrade six
    sudo ./setup.py
    sudo vi /etc/politraf/config.yaml
    sudo systemctl daemon-reload
    sudo systemctl start systat
    sudo systemctl start constat
    ```

    * OTX AlienVault - https://otx.alienvault.com
      * Create an account and select your feeds
      * Set API key in /etc/politraf/config.yaml
      * ./otxget.py
    
    * Censys.io - https://censys.io/
      * Create an account
      * Set API key in /etc/politraf/config.yaml
      * Set network to scan
      * ./ext_cscan.py

    ```
    sudo crontab -e
    0 2 * * * /opt/politraf/otxget.py >/dev/null 2>&1
    */2 * * * * /opt/politraf/iocwatch.py >/dev/null 2>&1
    0 2 * * * /opt/politraf/ext_cscan.py >/dev/null 2>&1
    ```
