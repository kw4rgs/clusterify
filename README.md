
![Clusterify_Logo](https://github.com/cristianzzzz/clusterify/blob/adc0167c2edc95ee3427b3b6ffa8a38930afb23f/logo.png)


# CLUSTERIFY

*"Uncover data patterns and relationships through clustering methods."*

Introducing Clusterify: A FastAPI App with K-means, Nearest Neighbor, and More!

Clusterify is a powerful FastAPI application that combines the strengths of K-means, Nearest Neighbor, Pandas, Numpy, and Python to supercharge your data clustering endeavors. By effortlessly processing your data points, Clusterify intelligently organizes and clusters them, meeting your specific needs with precision and speed.
With its user-friendly interface, Clusterify makes data clustering a breeze. Simply input your data, and let the magic happen. Whether you're dealing with massive datasets or real-time streams, Clusterify's robust architecture ensures optimal performance even under demanding scenarios.
Clusterify's secret weapon is the advanced K-means algorithm, which partitions your data into cohesive groups, revealing valuable patterns and similarities. Supported by Pandas and Numpy, Clusterify handles complex datasets effortlessly, providing you with insights to make informed decisions.
In addition, Clusterify incorporates the Nearest Neighbor technique to identify the closest matches for each data point within the clusters. This enables you to uncover hidden relationships and associations, empowering you to explore your data landscape like never before.
With the flexibility and extensibility of Python, Clusterify seamlessly integrates into your existing workflows. Whether you're an experienced data scientist or a coding enthusiast, Clusterify's clean codebase allows for easy customization and adaptation to suit your unique requirements.
Experience the future of data clustering with Clusterify. Unlock hidden potential, streamline decision-making, and gain a competitive edge in the ever-evolving field of data analysis. With Clusterify, your data becomes a gateway to deeper insights, revolutionizing the way you understand and leverage your information.

## Features 💪

-   Efficiently cluster and organize data points for improved data analysis and decision-making.
-   Utilize K-means algorithm to partition data into cohesive groups and identify patterns and similarities within the dataset.
-   Leverage Nearest Neighbor approach to identify closest matches for each data point, enabling the exploration of relationships and associations.
-   Seamlessly integrate with Pandas and Numpy for handling complex datasets with ease.
-   Offer a user-friendly interface to effortlessly submit data points and witness the clustering process in action.
-   Ensure robustness and scalability to handle large-scale datasets and real-time streams.
-   Provide flexibility and extensibility with a Python-based architecture for easy customization and integration into existing workflows.
-   Empower users, including data scientists and coding enthusiasts, to unlock hidden insights and make data-driven decisions with confidence.
-   Revolutionize the way data is analyzed and understood, transforming it into a powerful tool for gaining a competitive edge.
-   Redefine the boundaries of what's possible in data clustering, pushing the limits of technology to unleash the full potential of your data.

## Requirements 📝

**Hardware Requirements:**

A computer or server with sufficient processing power and memory to handle the size and complexity of your dataset. The exact requirements may vary depending on the scale of your data.
Software Requirements:

-   Python: Clusterify is built using Python, so you'll need a compatible version installed on your machine.
-   FastAPI: Ensure you have FastAPI, a modern, fast (high-performance) web framework for building APIs with Python, installed.
-   Pandas: Install the Pandas library to leverage its powerful data manipulation and analysis capabilities.
-   Numpy: Install Numpy, a fundamental package for scientific computing, to support advanced numerical operations.
-   Scikit-learn: Install Scikit-learn, a popular machine learning library, which includes the implementation of the K-means algorithm and nearest neighbor methods.

Any additional libraries or packages required for your specific data preprocessing, visualization, or analysis needs.

**Data Requirements:**

-   Prepare your data in a compatible format (e.g., CSV, JSON, or other structured formats) suitable for input into Clusterify.
-   Ensure the data points are appropriately formatted, with features or attributes that capture the relevant information for clustering.
-   It's worth noting that specific version requirements for Python, FastAPI, Pandas, Numpy, Scikit-learn, and other dependencies may vary. It's always recommended to refer to the documentation of each library for the latest version compatibility information.

Additionally, if you plan to deploy Clusterify on a server or in a production environment, you may need to consider additional requirements such as hosting infrastructure, security measures, and scalability considerations.

## Instructions 🚀

> I will use "ubuntu" for practical purposes..


To deploy and install your project, you can follow these instructions:

1. Update your system:
   ```
   sudo apt update
   ```

2. Upgrade installed packages:
   ```
   sudo apt upgrade
   ```

3. Install Python 3 virtual environment package:
   ```
   sudo apt install python3-venv
   ```

4. Navigate to the `/opt` directory:
   ```
   cd /opt
   ```

5. Clone the project repository from GitHub:
   ```
   git clone https://github.com/cristianzzzz/clusterify.git
   ```

6. Change to the project directory:
   ```
   cd /opt/clusterify
   ```

7. Create a Python virtual environment:
   ```
   python3 -m venv env
   ```

8. Activate the virtual environment:
   ```
   source env/bin/activate
   ```

9. Install the required build essentials (for K-means-constrained):
   ```
   sudo apt-get install build-essential
   ```

10. Install Python development headers (for K-means-constrained):
    ```
    sudo apt-get install python3-dev
    ```

11. Install the project dependencies using the requirements.txt file:
    ```
    pip install -r requirements.txt
    ```

12. Test the project by running it with Uvicorn:
    ```
    uvicorn clusterify:app --host 0.0.0.0 --port 8000 --workers 4
    ```

    Make sure to replace `clusterify:app` with the correct module and application object if needed.

Tip: To deactivate the virtual environment, simply type `deactivate` in the terminal.

To make the deployment process recursive, follow these additional steps:

1. Open the systemd service configuration file in a text editor:
   ```
   sudo nano /etc/systemd/system/clusterify.service
   ```

2. Paste the following content into the file:
   ```
   [Unit]
   Description=Clusterify FastAPI Application
   After=network.target

   [Service]
   User=<your_username>
   Group=<your_groupname>
   WorkingDirectory=/opt/clusterify
   ExecStart=/opt/clusterify/env/bin/uvicorn clusterify:app --host 0.0.0.0 --port 8000 --workers 4
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `<your_username>` and `<your_groupname>` with your actual username and group name.

3. Save the file and exit the text editor.

4. Enable the service to start on boot:
   ```
   sudo systemctl enable clusterify.service
   ```

5. Start the service:
   ```
   sudo systemctl start clusterify.service
   ```

Now, your application should be deployed and running as a systemd service. It will automatically start on boot and restart if it crashes.

## Information 📢

-   K-means is a clustering algorithm that tries to partition a set of points into K sets (clusters) such that the points in each cluster tend to be near each other. 
It is unsupervised because the points have no external classification.

-   K-nearest neighbors is a classification (or regression) algorithm that in order to determine the classification of a point, combines the classification of the K nearest points. 
It is supervised because you are trying to classify a point based on the known classification of other points.
