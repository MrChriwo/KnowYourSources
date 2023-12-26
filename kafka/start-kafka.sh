#!/bin/bash -e

KAFKA_DATA_DIR="/tmp/kafka-logs/"

if [ -f "${KAFKA_DATA_DIR}/meta.properties" ]; then
    echo "Deleting existing meta.properties file"
    rm "${KAFKA_DATA_DIR}/meta.properties"
fi

# Start Kafka
exec "/kafka/bin/kafka-server-start.sh" "/kafka/config/server.properties"
