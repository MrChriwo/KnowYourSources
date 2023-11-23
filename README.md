# KnowYourSources


### **Project Overview**

Welcome to the KnowYourSources project repository! This project aims to deliver a web application that allows users to upload exposes or abstracts of their scientific theses. The backend of the application utilizes Natural Language Processing (NLP) to analyze the uploaded abstracts. Based on the analysis, the backend then generates and returns a recommendation of the top 10 books related to the abstract.

### **Repository Structure**

1. **Lab Folder**

The "lab folder" is the core of the repository, where various components like modeling, crawlers, and other essential elements are developed. This is where the magic happens, and the backend processes are fine-tuned to provide accurate and relevant book recommendations.


2. **Frontend Folder** 

The "frontend" folder contains the web application's user interface. It is built using React, Vite, and TypeScript, providing a modern and responsive interface for users to interact with the KnowYourSources platform. This is the client-facing part of the application where users can upload their scientific abstracts.

3. **Frontend Folder** 

The "backend" folder is responsible for handling the server-side logic. It utilizes the Django framework to deliver endpoints that cater to user services and the essential endpoint for users to submit their text and receive book recommendations. The backend ensures seamless communication between the frontend and the core processing in the lab folder.