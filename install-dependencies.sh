#!/bin/bash
mkdir /etc/politraf
cp config/config.yaml /etc/politraf/config.yaml
mkdir /opt/politraf
cp config/systat.service /etc/systemd/system/systat.service
cp config/constat.service /etc/systemd/system/constat.service
cp systat.py /opt/politraf/systat.py
cp otxget.py /opt/politraf/otxget.py
cp constat.py /opt/politraf/constat.py
cp dbmodels.py /opt/politraf/dbmodels.py
sudo service clickhouse-server start
