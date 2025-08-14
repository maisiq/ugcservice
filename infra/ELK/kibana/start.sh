#!/bin/bash

bin/kibana-keystore create
cat /run/secrets/kibana_es_username | bin/kibana-keystore add elasticsearch.username --stdin
cat /run/secrets/kibana_es_pw | bin/kibana-keystore add elasticsearch.password --stdin

exec /usr/local/bin/kibana-docker