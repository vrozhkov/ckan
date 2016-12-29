#!/usr/bin/env bash


cd /home/user/ckan/lib/default/src/ckan
/home/user/ckan/lib/default/bin/paster serve /home/user/ckan/etc/default/development.ini > output.log 2>&1
