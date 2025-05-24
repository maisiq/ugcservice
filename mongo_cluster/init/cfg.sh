#!/bin/bash

set -e

# Main process
mongod --configsvr --replSet mongors1conf --port 27017 --bind_ip_all --auth --keyFile /keys/mongo-keyfile &

# Replica set initialization
CFG_NODES=("mongocfg1" "mongocfg2" "mongocfg3")

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

for node in "${CFG_NODES[@]}"; do
    wait_for_mongo "$node"
done

mongosh --quiet <<EOF
rs.initiate({
    _id: "mongors1conf",
    configsvr: true,
    members: [
        { _id: 0, host: "${CFG_NODES[0]}:27017" },
        { _id: 1, host: "${CFG_NODES[1]}:27017" },
        { _id: 2, host: "${CFG_NODES[2]}:27017" }
    ]
})
EOF

echo "🟢 CFG INIT COMPLETED"

wait -n
