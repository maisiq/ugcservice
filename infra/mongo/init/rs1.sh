#!/bin/bash

set -e

# Main process
mongod --shardsvr --replSet mongors1 --dbpath /data/db --port 27017 --bind_ip_all --auth --keyFile /keys/mongo-keyfile &

# Replica set initialization
RS1_NODES=("mongors1n1" "mongors1n2" "mongors1n3")

MAX_ATTEMPTS=20
SLEEP_TIME=15

function wait_for_mongo {
    local server="$1"
    local attempt=1
    echo "Ожидание доступности MongoDB на ${server}..."
    
    while (( attempt <= MAX_ATTEMPTS )); do
        if echo "db.runCommand({ping:1})" | mongosh --quiet --host "$server" --eval "quit()" 2>/dev/null; then
            echo "MongoDB на ${server} доступен."
            return 0
        fi
        echo "[${server}] Попытка ${attempt}/${MAX_ATTEMPTS} не удалась. Ожидание ${SLEEP_TIME} сек..."
        sleep $SLEEP_TIME
        ((attempt++))
    done
    
    echo "Ошибка: Сервер ${server} недоступен после ${MAX_ATTEMPTS} попыток."
    exit 1
}


for host in "${RS1_NODES[@]}"; do
    wait_for_mongo "$host"
done

mongosh --quiet <<EOF
rs.initiate({
    _id: "mongors1",
    members: [
        { _id: 0, host: "${RS1_NODES[0]}:27017" },
        { _id: 1, host: "${RS1_NODES[1]}:27017" },
        { _id: 2, host: "${RS1_NODES[2]}:27017" }
    ]
})
EOF

# Waiting until node become primary
until mongosh "mongodb://localhost:27017/?replicaSet=mongors1" --quiet --eval 'db.isMaster().ismaster' | grep -q 'true'; do
    sleep 2
done

# Create root user
mongosh --quiet <<EOF
    db.getSiblingDB("admin").createUser({
        user: "$(</run/secrets/mongo-root-user)", 
        pwd: "$(</run/secrets/mongo-root-pwd)", 
        roles: ["root"]
    })
EOF

echo "🟢 RS1 INIT COMPLETED"

wait -n
