# PowerShell script to start the compose services 
# and restart Kafka broker services if needed
# if there is no nginx.conf file, it will rename the nginx_template to nginx.conf
# according to that make sure you replace the api key in the template to your own api key

# Usage: .\start_services.ps1 -DEPLOYMENT_SERVER_NAME "example.com" -QDRANT_COLLECTION_NAME "knowyoursources"
# make sure you have docker and docker-compose installed

# example: .\start_services.ps1 -DEPLOYMENT_SERVER_NAME "example.com" -QDRANT_COLLECTION_NAME "knowyoursources" -KAGGLE_SOURCE "Cornell-University/arxiv" -TARGET_CRAWL_COLS "headline", "publish_date" -API_KEY "your_api_key"
# replace example.com with your own server name / ip ( or localhost for local development) 
# replace knowyoursources with your own collection name
# replace Cornell-University/arxiv with your own kaggle source
# replace the target crawl cols with your own target crawl cols
# replace your_api_key with your own api key

# GitHub: MrChriwo

param (
    [string]$DEPLOYMENT_SERVER_NAME,
    [string]$QDRANT_COLLECTION_NAME, 
    [string]$KAGGLE_SOURCE,
    [string[]]$TARGET_CRAWL_COLS,
    [string]$API_KEY
)

# Set environment variables
$env:DEPLOYMENT_SERVER_NAME = $DEPLOYMENT_SERVER_NAME
$env:QDRANT_COLLECTION_NAME = $QDRANT_COLLECTION_NAME
$env:KAGGLE_SOURCE = $KAGGLE_SOURCE
$env:TARGET_CRAWL_COLS = $TARGET_CRAWL_COLS
$env:API_KEY = $API_KEY

# Check if nginx.conf exists
$nginxConfPath = Join-Path $PSScriptRoot "nginx.conf"

if (-not (Test-Path $nginxConfPath)) {
    # If nginx.conf doesn't exist, rename nginx_template to nginx.conf

    $nginxTemplatePath = Join-Path $PSScriptRoot "nginx_template"
    
    if (Test-Path $nginxTemplatePath) {
        Rename-Item -Path $nginxTemplatePath -NewName $nginxConfPath
        Write-Host "Renamed 'nginx_template' to 'nginx.conf'."
    } else {
        Write-Host "'nginx_template' not found."
    }
} else {
    Write-Host "'nginx.conf' already exists."
}

# Function to check and restart Kafka broker services
function Restart-KafkaServices {
    $maxRetries = 6
    $retryCount = 0

    write-host "Checking Kafka broker services..."

    $brokerContainers = @("knowyoursources-kafka-1", "knowyoursources-kafka-2")

    foreach ($container in $brokerContainers) {
        Start-Sleep -Seconds 10

        write-host "Checking '$container' container status..."
        do {
            # Check if the container is running
            $containerStatus = docker inspect --format '{{.State.Status}}' $container

            if ($containerStatus -ne 'running') {
                # Restart the container
                Write-Host "Restarting '$container' container..."
                docker restart $container

                # Increment the retry count
                $retryCount++
                Start-Sleep -Seconds 16  # Adjust the sleep duration as needed
            } else {
                Write-Host "'$container' container is running."
                break  # Exit the loop if container is running
            }
        } while ($retryCount -lt $maxRetries)
    }

    # Exit with code 1 if any container restarts failed after max retries
    if ($retryCount -ge $maxRetries) {
        Write-Host "Failed to restart Kafka containers after $maxRetries attempts. Exiting with code 1."
        exit 1
    }
}

# Run Docker Compose
docker compose up -d --build

# Check and restart Kafka broker services
Restart-KafkaServices

$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
$relativePath = ".\ascii_art.txt"

# Combine the script directory and relative path to get the full path
$asciiArtFilePath = Join-Path -Path $scriptDirectory -ChildPath $relativePath

# Use Get-Content to read the file content and display it
Get-Content $asciiArtFilePath