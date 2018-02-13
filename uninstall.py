#!/usr/bin/python3
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

from subprocess import call
import shutil
import os


green='\033[32m'
greene='\033[0m'
orange='\033[33m'
orangee='\033[0m'
blue='\033[34m'

try:
    print (green + "Stop Politraf" + greene)
    call(["systemctl", "stop" , "systat"])
    call(["systemctl", "stop" , "constat"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green + "Stop Clickhouse and Grafana" + greene)
    call(["service", "clickhouse-server" , "stop"])
    call(["service", "grafana-server" , "stop"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green +'Remove services' + greene)
    shutil.move('/etc/systemd/system/systat.service', '/opt/politraf')
    shutil.move('/etc/systemd/system/constat.service', '/opt/politraf')
    call(["systemctl", "daemon-reload"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green + 'Uninstall Clickhouse and Grafana' + greene)
    call(["apt-get", "remove" , "grafana"])
    call(["apt-get", "remove" , "clickhouse-client" , "clickhouse-server-common"])
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)

try:
    print (green +"Remove politraf" + greene)
    shutil.rmtree("/opt/politraf")
    shutil.rmtree("/etc/politraf")
    print (green + 'Done' + greene)
except Exception as e:
    print(orange, e, orangee)