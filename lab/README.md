## **Lab**

Welcome to the Lab, the beating heart of the repository! This is the central hub where we develop and refine cutting-edge features that will power our backend services. Whether it's crafting machine-learning models, building crawlers, or developing various tools, this lab is where our innovation takes center stage.

### **Usage**

To create a development environment, we've set up a .devcontainer configuration that provides a complete Python development environment. Here's a step-by-step guide to getting started:

1.  **install docker** ensure that you have Docker Desktop or the Docker Engine installed on your local machine. You can download it from [here](https://www.docker.com/products/docker-desktop/)

2.  **install VS Code Extension** Install the "Dev - Containers " extension for Visual Studio Code. If you don't have it yet, you can find it by searching for

        ms-vscode-remote.remote-containers

    in the Extensions view of VS Code. Install the extension.

3.  **Reopen in Container** After installing the extension, ensure that your Docker Desktop is running and look for a blue button in the bottom left corner of VS Code. Click on it and select "Reopen in Container." This initiates the development environment in a new VS Code window.

### **Install new dependencies / packages**

Within the container environment, leverage the convenience of the install.sh script to effortlessly add new dependencies to the development environment. This script streamlines the process by installing packages via pip and seamlessly updating the requirements.txt file.

This approach ensures that the dependencies are clearly documented in the requirements.txt file, maintaining a well-defined and reproducible development environment. Simply execute the script as needed to extend the environment with additional Python packages. You can execute the script with the following command

            sh install.sh your_package_name

replace "your_package_name" with the needed package like pandas, numpy etc.

Happy coding :)
