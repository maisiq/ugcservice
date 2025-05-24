#!/bin/bash

set -e

if [ ! -f "mongodb-keyfile" ]; then 
    openssl rand -base64 756 > mongodb-keyfile
    chmod 600 mongodb-keyfile
fi

mongod --replSet rs0 --bind_ip_all --auth --keyFile mongodb-keyfile &

until mongosh > /dev/null; do
    echo "❗ Mongosh не отвечает. Повторная проверка через 5 секунд..."
    sleep 5
done

echo "rs.initiate()" | mongosh

mongosh --quiet <<EOF
    db.getSiblingDB("admin").createUser({
        user: "root", 
        pwd: "example", 
        roles: ["root"]
    })
EOF

echo "🟢 Replica set is ready..."

wait -n
