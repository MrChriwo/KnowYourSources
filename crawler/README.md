# Crawler Service


### Overview
The Crawler service is designed to download datasets from Kaggle, read the data from files (in either JSON or CSV format), and subsequently push the data to a Kafka topic. This service facilitates the extraction and ingestion of information from Kaggle datasets, allowing for further processing and analysis.

Usage
To use the Crawler service, the following command-line arguments can be specified:

```sh
python main.py --source <source_name> --target <target_column> [--workers <num_workers>] [--logfile <log_file>]
```

### Arguments:

--source: Defines the source dataset on Kaggle. This argument is optional, and if not provided, the service will prompt for user input.

--target: Defines the target column(s) to crawl. Multiple target columns can be specified by separating them with spaces.

--workers: Defines the number of crawler workers. This argument is optional, and the default value is set to 1 if not specified

(**workers currently not supported.**).

--logfile: Defines the log file where crawler activity and errors are logged. This argument is optional, and the default log file is set to "crawler.log" if not specified.


### Kaggle Credentials:

For the Crawler service to access Kaggle datasets, a kaggle.json file containing your Kaggle username and API key must be placed in the .kaggle folder in your home directory. Ensure that the Kaggle credentials are correctly configured to enable the service to download datasets seamlessly.

### Example

```bash
python main.py --source dataset_name --target column1 column2 --workers 3 --logfile crawler_output.log
```

This example downloads the specified dataset from Kaggle, crawls the specified target columns, uses three crawler workers, and logs the activity to a file named "crawler_output.log."

### **Note:**

Ensure that you have the required dependencies installed before running the Crawler service.
Make sure to place the kaggle.json file in the .kaggle folder with your Kaggle credentials.
For more details on the available options and functionality, check out the scripts. 


