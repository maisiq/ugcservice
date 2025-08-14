#!/bin/bash

if [ ! -f ~/config/logstash.keystore ]; then
    bin/logstash-keystore create
    cat /run/secrets/logstash_es_user | bin/logstash-keystore add ES_USER --stdin
    cat /run/secrets/logstash_es_password | bin/logstash-keystore add ES_PW --stdin
fi

exec logstash --config.reload.automatic -f /config/logstash.conf