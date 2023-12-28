
![KYS](https://github.com/MrChriwo/KnowYourSources/assets/96289753/e97b134e-b970-434a-986f-1f4113835318)


# Table of Contents

- [🙋‍♂️ Introduction](#introduction)
- [🔎 Repository Overview](#repository-overview)
  - [Lab Folder](#lab-folder)
  - [Frontend Folder](#frontend-folder)
  - [Backend Folder](#backend-folder)
  - [Kafka Folder](#kafka-folder)
  - [Embedding Service](#embedding-service)
  - [Crawler](#crawler-folder)
  - [Start Service Scripts](#start-services-scripts)
    - [Description](#script-description)
    - [Usage](#usage)
- [💡 NLP Model](#nlp-model)
- [💻 Testing and Self-deployment](#testing-and-deployment)


 # Introduction

Welcome to the KnowYourSources project repository, a groundbreaking initiative designed to empower users in the academic community. Our primary goal is to create a user-friendly web application that facilitates the sharing and exploration of scientific theses. Users can easily upload exposes or abstracts of their research, opening the door to a wealth of knowledge and insights.

At the heart of our application is a sophisticated backend powered by Natural Language Processing (NLP) technology. This enables us to analyze the uploaded abstracts. Based on this analysis, the backend dynamically generates and returns personalized recommendations for the top 10 books that are closely related to the content of the abstract.

Behind the scenes, our system employs an automated web crawler to fetch a rich dataset from Kaggle. This dataset is seamlessly integrated into our workflow and serves as the foundation for the recommendation engine. The crawler gathers relevant information and pushes it to a Kafka cluster, featuring two brokers and a Zookeeper for enhanced scalability and fault tolerance.

Furthermore, we have implemented a dedicated embedding service that acts as a Kafka consumer. This service reads the crawled messages and calculates embeddings representations of the textual content. Once a message has been embedded, the resulting vector is stored in a Qdrant vector database. This specialized database enables efficient similarity searches, allowing users to explore related abstracts and discover connections between different scientific works.


# Repository Overview

## Lab Folder

The "lab" folder is the core of the repository, where various components like modeling, crawlers, and other essential elements are developed. This is where the magic happens, and the backend processes are fine-tuned to provide accurate and relevant book recommendations.


## Frontend-Folder 

The "frontend" folder contains the web application's user interface. It is built using React, Vite, and TypeScript, providing a modern and responsive interface for users to interact with the KnowYourSources platform. This is the client-facing part of the application where users can upload their scientific abstracts.


## Backend Folder

The "backend" folder is responsible for handling the server-side logic. It utilizes the Django framework to deliver endpoints that cater to user services and the essential endpoint for users to submit their text and receive book recommendations. The backend ensures seamless communication between the frontend and the core processing in the lab folder.


## Kafka Folder

Within this directory, you'll find the essential configuration files for every Kafka broker and its associated Zookeeper service. As the cluster operates, a designated "data" folder is dynamically generated, ensuring persistent data storage capabilities even in the event of system restarts. This meticulous organization guarantees a seamless and reliable operation of the Kafka cluster, with configurations tailored for optimal performance and durability.

## Embedding Service

Actually the core of our NLP Service! This source code, designed to function as a Kafka consumer, plays an essential role in our system. Operating in batch mode, it efficiently reads incoming messages and seamlessly pushes the corresponding embeddings to the QDrant Vector Database. This critical component ensures that the extracted embeddings are swiftly and accurately integrated into the database.

## Crawler Folder 

The crawler folder encapsulates a vital component of our system, responsible for systematically acquiring data to fuel our knowledge repository. Specifically, the crawler is designed to download a designated dataset from Kaggle, a prominent platform for data science and machine learning resources. This data is then seamlessly transformed into JSON structures and dispatched to our Kafka cluster, forming a crucial part of our project pipeline. The dockerized crawler's functionality is configurable through command-line arguments specified within its Dockerfile.

To ensure data persistence, the crawler integrates an SQLite database, utilizing a 'current_jobs' table to meticulously store the progress of dataset processing. This mechanism proves especially beneficial when dealing with datasets that undergo updates on Kaggle. Upon rerunning the crawler on an augmented dataset, it selectively pushes only the new data to the Kafka/project pipeline, ensuring efficiency and avoiding unnecessary duplication.

Furthermore, the crawler boasts a robust logging service that captures and records valuable information about its operations. These logs are intelligently stored in a file, with the option to mount the file via Docker Compose volume. This logging feature enhances traceability and aids in troubleshooting, enabling a comprehensive understanding of the crawler's behavior and performance. As we continuously refine and optimize our data acquisition processes, the crawler stands as a pivotal element in ensuring the currency and relevance of our knowledge base.

## Start Services Scripts 

### Script Description
The start_services scripts play a pivotal role in the seamless deployment of our KnowYourSources application, offering convenience for both Windows and Linux/Unix users. The start_services.ps1 script is tailored for Windows systems, while start_services.sh is designed for Linux/Unix environments. These scripts come equipped with parameters allowing users to specify the host on which the application runs.

One notable feature of these scripts is their adaptability to varying nginx configurations. In the absence of an existing nginx.conf file, the scripts intelligently employ the nginx template file as the default configuration. This flexibility streamlines the setup process, ensuring a consistent and reliable deployment experience.

To address potential challenges with Kafka broker container stability, the scripts incorporate a robust workaround. They systematically check the status of both brokers, and in the event of a crash, the scripts automatically restart them. This proactive approach helps maintain the integrity and reliability of the Kafka cluster, ensuring continuous and uninterrupted operation.

In summary, the start_services scripts serve as user-friendly entry points for deploying KnowYourSources, accommodating different operating systems and gracefully handling potential Kafka broker disruptions. Their parameterization and adaptive configuration handling contribute to a smooth deployment experience, underscoring our commitment to providing a reliable and hassle-free application environment.

**Note** 
It's important to note that the start_services.sh script is equipped with Windows line endings, and as such, it requires conversion using tools like dos2unix to ensure compatibility with Linux/Unix systems. This step becomes crucial for a seamless execution of the script on Linux/Unix platforms, as these systems expect different line endings compared to Windows.


To install dos2unix on a Linux system using apt (Advanced Package Tool), you can use the following commands:

```bash
sudo apt update -y
sudo apt install -y dos2unix
```

Once installed, you can use dos2unix to convert a file. Here's an example command:


(Assuming that you run the command inside the KnowYourSources Directory) 

```bash
dos2unix start_services.sh
```

### Usage

Example how to run the services on windows machine (.ps1 script): 

```powershell
.\start_services.ps1 -DEPLOYMENT_SERVER_NAME "example.com" -QDRANT_COLLECTION_NAME "knowyoursources" -KAGGLE_SOURCE "Cornell-University/arxiv"" -TARGET_CRAWL_COLS "title" "abstract"
```

Example how to run the services on linux systems (.sh script): 
```bash
bash ./start_services.sh "localhost" "knowyoursources" "Cornell-University/arxiv" "title abstract"```

# NLP Model

In the initial version of our tool, we have implemented the SPECTER transformer model for calculating embeddings. It's essential to note that this choice is primarily for prototyping purposes, allowing us to quickly integrate a functional system and gather valuable insights. As part of our ongoing development, we are actively engaged in the selection and evaluation of various transformer models to ensure the optimal performance and accuracy of our recommendation engine. The process involves a comprehensive assessment of different models, considering factors such as efficiency, precision, and scalability. This iterative approach reflects our commitment to delivering a robust and well-optimized solution, and we anticipate refining our model selection based on rigorous evaluation and testing in the upcoming stages of development.

# Testing and deployment

To deploy the application locally or on your preferred hosting environment, feel free to clone or fork the repository at any time. We've streamlined the deployment process using Docker Compose, harnessing the versatility of Docker to ensure a consistent experience across various platforms.

For Windows systems, simply execute the start_services.ps1 script with the relevant parameters. Meanwhile, Linux and Unix users can run the start_services.sh script. Both scripts come with a comprehensive usage tutorial, complete with examples, to guide you through the process.

Should you choose to fork the repository and deploy the application on your server, you can leverage the integrated GitHub Actions for deployment CI/CD. To enable this, ensure you add the necessary secrets outlined in the deployment.yml file to your repository. This will enable a seamless deployment process, allowing you to focus on maximizing the potential of the KnowYourSources application on your server. 
