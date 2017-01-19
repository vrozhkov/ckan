#!/usr/bin/env bash

# service jetty8 restart

cd /usr/lib/ckan/default/src/ckan
/usr/lib/ckan/default/bin/paster serve /etc/ckan/default/development.ini > output.log 2>&1
