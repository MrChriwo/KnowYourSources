# PowerShell script to start the compose services 
# and restart Kafka broker services if needed
# if there is no nginx.conf file, it will rename the nginx_template to nginx.conf
# according to that make sure you replace the api key in the template to your own api key

# Usage: .\start_services.ps1 -SERVER_NAME <SERVER_NAME> -QDRANT_COLLECTION_NAME <QDRANT_COLLECTION_NAME>
# make sure you have docker and docker-compose installed

# Example: .\start_services.ps1 -DEPLOYMENT_SERVER_NAME "example.com" -QDRANT_COLLECTION_NAME "knowyoursources"
# replace example.com with your own server name or localhost for local development

# GitHub: Mr_Chriwo

param (
    [string]$DEPLOYMENT_SERVER_NAME,
    [string]$QDRANT_COLLECTION_NAME
)

# Set environment variables
$env:DEPLOYMENT_SERVER_NAME = $DEPLOYMENT_SERVER_NAME
$env:QDRANT_COLLECTION_NAME = $QDRANT_COLLECTION_NAME

# Check if nginx.conf exists
$nginxConfPath = Join-Path $PSScriptRoot "nginx.conf"

if (-not (Test-Path $nginxConfPath)) {
    # If nginx.conf doesn't exist, rename nginx_template to nginx.conf

    $nginxTemplatePath = Join-Path $PSScriptRoot "nginx_template"
    
    if (Test-Path $nginxTemplatePath) {
        Rename-Item -Path $nginxTemplatePath -Destination $nginxConfPath
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