#!/bin/bash

set -e

KIBANA_PASSWORD=$(cat /run/secrets/kibana_es_pw)
KIBANA_USER=$(cat /run/secrets/kibana_es_username)

/usr/local/bin/docker-entrypoint.sh eswrapper &

until curl -u "${ELASTIC_USER}:${ELASTIC_PASSWORD}" -sSf "http://localhost:9200" > /dev/null; do
    echo "❗ Elasticsearch не отвечает. Повторная проверка через 10 секунд..."
    sleep 10
done

COMMANDS="$(printf "%s\n%s" "$KIBANA_PASSWORD" "$KIBANA_PASSWORD")"

echo "$COMMANDS" | elasticsearch-reset-password -u $KIBANA_USER -b -i

echo "🟢 Пароль для KIBANA успешно задан"

wait -n
