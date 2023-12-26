#!/bin/bash


# bash script to start the compose services 
# and restart Kafka broker services if needed
# if there is no nginx.conf file, it will rename the nginx_template to nginx.conf
# according to that make sure you replace the api key in the template to your own api key

# Usage: sh .\start_services.sh <SERVER_NAME> <QDRANT_COLLECTION>
# make sure you have docker and docker-compose installed

# Example: .\start_services.ps1 "example.com" "myCollection"
# replace example.com with your own server name or localhost for local development

# GitHub: Mr_Chriwo

SERVER_NAME=$1
QDRANT_COLLECTION=$2

export DEPLOYMENT_SERVER_NAME=$SERVER_NAME
export QDRANT_COLLECTION=$QDRANT_COLLECTION

nginxConfPath="./nginx.conf"

if [ ! -f "$nginxConfPath" ]; then
    # If nginx.conf doesn't exist, rename nginx_template to nginx.conf
    nginxTemplatePath="./nginx_template"

    if [ -d "$nginxTemplatePath" ]; then
        mv "$nginxTemplatePath" "$nginxConfPath"
        echo "Renamed 'nginx_template' to 'nginx.conf'."
    else
        echo "'nginx_template' not found."
    fi
else
    echo "'nginx.conf' already exists."
fi

restart_kafka_services() {
    maxRetries=6
    retryCount=0

    brokerContainers=("knowyoursources-kafka-1" "knowyoursources-kafka-2")

    echo "Checking Kafka broker services..."

    for container in "${brokerContainers[@]}"; do
        sleep 10

        echo "Checking '$container' container status..."
        while [ $retryCount -lt $maxRetries ]; do
            # Check if the container is running
            containerStatus=$(docker inspect --format '{{.State.Status}}' "$container")

            if [ "$containerStatus" != "running" ]; then
                echo "Restarting '$container' container..."
                docker restart "$container"

                ((retryCount++))
                sleep 16 
            else
                echo "'$container' container is running."
                break 
            fi
        done

        if [ $retryCount -ge $maxRetries ]; then
            echo "Failed to restart Kafka containers after $maxRetries attempts. Exiting with code 1."
            exit 1
        fi
    done
}

# Run Docker Compose
docker compose up -d --build

# Check and restart Kafka broker services
restart_kafka_services
cat "ascii_art.txt"
