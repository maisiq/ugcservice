#!/bin/bash
set -e  # Прерывать выполнение скрипта при ошибке

# Установка необходимых пакетов
apt-get update && apt-get install -y wget
wget -qO- https://www.mongodb.org/static/pgp/server-8.0.asc | tee /etc/apt/trusted.gpg.d/server-8.0.asc
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list
apt-get update && apt-get install -y mongodb-mongosh

# Определение переменных
RS1_SERVER="mongors1n3"
RS2_SERVER="mongors2n3"
CFG_SERVER="mongocfg3"
MONGOS_1="mongos1"
MAX_ATTEMPTS=20
SLEEP_TIME=30

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

# Инициализация реплики 1
wait_for_mongo "$RS1_SERVER"
echo '
rs.initiate({
    _id: "mongors1",
    members: [
        { _id: 0, host: "mongors1n1:27017" },
        { _id: 1, host: "mongors1n2:27017" },
        { _id: 2, host: "mongors1n3:27017" }
    ]
})' | mongosh --quiet --host "$RS1_SERVER"
echo "RS1 INIT COMPLETED"

# Инициализация реплики 2
wait_for_mongo "$RS2_SERVER"
echo '
rs.initiate({
    _id: "mongors2",
    members: [
        { _id: 0, host: "mongors2n1:27017" },
        { _id: 1, host: "mongors2n2:27017" },
        { _id: 2, host: "mongors2n3:27017" }
    ]
})' | mongosh --quiet --host "$RS2_SERVER"
echo "RS2 INIT COMPLETED"

# Инициализация конфигурационной реплики
wait_for_mongo "$CFG_SERVER"
echo '
rs.initiate({
    _id: "mongors1conf",
    members: [
        { _id: 0, host: "mongocfg1:27017" },
        { _id: 1, host: "mongocfg2:27017" },
        { _id: 2, host: "mongocfg3:27017" }
    ]
})' | mongosh --quiet --host "$CFG_SERVER"
echo "mongors1conf INIT COMPLETED"

# Инициализация шардинга
wait_for_mongo "$MONGOS_1"
echo 'sh.addShard("mongors1/mongors1n1:27017")' | mongosh --quiet --host "$MONGOS_1"
echo 'sh.addShard("mongors2/mongors2n1:27017")' | mongosh --quiet --host "$MONGOS_1"
echo 'sh.shardCollection("movies.movies", { _id: "hashed" }, { numInitialChunks: 5 })' | mongosh --quiet --host "$MONGOS_1"
echo "${MONGOS_1} INIT COMPLETED"
