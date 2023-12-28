
![KYS](https://github.com/MrChriwo/KnowYourSources/assets/96289753/e97b134e-b970-434a-986f-1f4113835318)

## **Project Overview**


Welcome to the KnowYourSources project repository, a groundbreaking initiative designed to empower users in the academic community. Our primary goal is to create a user-friendly web application that facilitates the sharing and exploration of scientific theses. Users can easily upload exposes or abstracts of their research, opening the door to a wealth of knowledge and insights.

At the heart of our application is a sophisticated backend powered by Natural Language Processing (NLP) technology. This enables us to analyze the uploaded abstracts. Based on this analysis, the backend dynamically generates and returns personalized recommendations for the top 10 books that are closely related to the content of the abstract.

Behind the scenes, our system employs an automated web crawler to fetch a rich dataset from Kaggle. This dataset is seamlessly integrated into our workflow and serves as the foundation for the recommendation engine. The crawler gathers relevant information and pushes it to a Kafka cluster, featuring two brokers and a Zookeeper for enhanced scalability and fault tolerance.

Furthermore, we have implemented a dedicated embedding service that acts as a Kafka consumer. This service reads the crawled messages and calculates embeddings representations of the textual content. Once a message has been embedded, the resulting vector is stored in a Qdrant vector database. This specialized database enables efficient similarity searches, allowing users to explore related abstracts and discover connections between different scientific works.


## **Repository Structure**

Lab Folder

The "lab" folder is the core of the repository, where various components like modeling, crawlers, and other essential elements are developed. This is where the magic happens, and the backend processes are fine-tuned to provide accurate and relevant book recommendations.


#### Frontend Folder 

The "frontend" folder contains the web application's user interface. It is built using React, Vite, and TypeScript, providing a modern and responsive interface for users to interact with the KnowYourSources platform. This is the client-facing part of the application where users can upload their scientific abstracts.


#### Backend Folder

The "backend" folder is responsible for handling the server-side logic. It utilizes the Django framework to deliver endpoints that cater to user services and the essential endpoint for users to submit their text and receive book recommendations. The backend ensures seamless communication between the frontend and the core processing in the lab folder.


#### Kafka Folder

Within this directory, you'll find the essential configuration files for every Kafka broker and its associated Zookeeper service. As the cluster operates, a designated "data" folder is dynamically generated, ensuring persistent data storage capabilities even in the event of system restarts. This meticulous organization guarantees a seamless and reliable operation of the Kafka cluster, with configurations tailored for optimal performance and durability.

#### mbedding_service

Actually the core of our NLP Service! This source code, designed to function as a Kafka consumer, plays an essential role in our system. Operating in batch mode, it efficiently reads incoming messages and seamlessly pushes the corresponding embeddings to the QDrant Vector Database. This critical component ensures that the extracted embeddings are swiftly and accurately integrated into the database.

## **Testing and self-deployment**


To deploy the application locally or on your preferred hosting environment, feel free to clone or fork the repository at any time. We've streamlined the deployment process using Docker Compose, harnessing the versatility of Docker to ensure a consistent experience across various platforms.

For Windows systems, simply execute the start_services.ps1 script with the relevant parameters. Meanwhile, Linux and Unix users can run the start_services.sh script. Both scripts come with a comprehensive usage tutorial, complete with examples, to guide you through the process.

Should you choose to forge your own repository and deploy the application on your server, you can leverage the integrated GitHub Actions for deployment CI/CD. To enable this, ensure you add the necessary secrets outlined in the deployment.yml file to your repository. This will enable a seamless deployment process, allowing you to focus on maximizing the potential of the KnowYourSources application on your server. 
