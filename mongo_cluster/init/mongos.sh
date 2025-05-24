#!/bin/bash

set -e

# Main process
mongos --configdb mongors1conf/mongocfg1:27017,mongocfg2:27017,mongocfg3:27017 --port 27017 --bind_ip_all --keyFile /keys/mongo-keyfile &

# Replica set initialization
RS1_NODES=("mongors1n1" "mongors1n2" "mongors1n3")
RS2_NODES=("mongors2n1" "mongors2n2" "mongors2n3")
CFG_NODES=("mongocfg1" "mongocfg2" "mongocfg3")
MONGOS="mongos1"  # Should also wait for mongos(self) instance

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


for host in "${RS1_NODES[@]}" "${RS2_NODES[@]}" "${CFG_NODES[@]}" "$MONGOS"; do
    wait_for_mongo "$host"
done


echo "sh.addShard(\"mongors1/mongors1n1:27017\");" | mongosh
echo "sh.addShard(\"mongors2/mongors2n1:27017\");" | mongosh

mongosh --quiet <<EOF
    db.getSiblingDB("admin").createUser({
        user: "$(</run/secrets/mongo-root-user)", 
        pwd: "$(</run/secrets/mongo-root-pwd)", 
        roles: ["root"]
    })
EOF

mongosh "mongodb://$(</run/secrets/mongo-root-user):$(</run/secrets/mongo-root-pwd)@localhost:27017/?authSource=admin" <<EOF
    sh.shardCollection(
        "movies.movies", 
        { _id: "hashed" }, 
        { numInitialChunks: 5 }
    );
EOF

echo "🟢 MONGOS INIT COMPLETED"

wait -n
