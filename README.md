# From Query to Information: An Advanced Information Retrieval System Trained on Wikipedia

## Overview
We have developed an advanced information retrieval system designed to deliver accurate and comprehensive results using Wikipedia as the primary data source. The system leverages state-of-the-art machine learning models and natural language processing techniques to return precise information for various types of queries.

For more detailed information about the system's design and implementation, refer to our paper [here](report/An_Advanced_Information_Retrieval_System_Trained_on_Wikipedia.pdf).

## Features
- **Accurate Results:** Leveraging machine learning models trained on Wikipedia for accurate information retrieval.
- **Natural Language Understanding:** Ability to understand complex natural language queries.
- **Scalability:** Works well across a wide range of data sizes.

### Data Pipeline
![Data Pipeline](flowcharts/pipeline.png)
A visualization of the data pipeline used in our system.

### Language Model
![Language Model](flowcharts/language_model.png)
Diagram showing the architecture of the language model.

### Query Processing
![Query Processing](flowcharts/query.png)
Flowchart of the query processing workflow within the system.

## Demo Video
For a quick demonstration of how the system works, check out our demo video [here](demo/Demo.mov).

## Results

1. **Question:**  What is Mobile DevOps?

   **Answer:** Mobile DevOps is a set of practices that applies
the principles of DevOps specifically to the development of mobile applications. Mobile DevOps is not simply as a branch of DevOps specific to mobile app development, instead an extension and reinterpretation of the DevOps philosophy due to very specific requirements of the
mobile world.

2. **Question:**  What is computer science?
   
   **Answer:** Computer science is the study of computation, information, and automation. Computer science spans theoretical disciplines (such as algorithms, theory of computation, and information theory) to applied disciplines (including the design and implementation of hardware and software). Computer science is closely related to computer programming. Algorithms and data structures are central to computer science.

3. **Question:**  Explain to me what is K-Means Clustering
   
   **Answer:** k-means clustering is a method to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean. This results in a partitioning of the data space into Voronoi cells. k-means clustering minimizes within-cluster variances (squared Euclidean distances). efficient heuristic algorithms converge quickly to a local optimum. L-means clustering tends to find clusters of comparable spatial extent

4. **Question:** What is Data Science?
   
   **Answer:** Data science is an interdisciplinary academic field that uses statistics, scientific computing, scientific methods, processes, algorithms and systems to extract or extrapolate knowledge and insights from potentially noisy, structured, or unstructured data. Data science also integrates domain knowledge from the underlying application domain (e.g., natural sciences, information technology, and medicine). It uses techniques and theories drawn from many fields within the context of mathematics, statistics, computer science, information science, and domain knowledge.

6. **Question:** Say something about support vector machine
   
   **Answer:** In machine learning, support vector machines are supervised max-margin models with associated learning algorithms that analyze data for classification and regression analysis. SVMs are one of the most studied models. SVMs can efficiently perform a non-linear classification using what is called the kernel trick, SVMs can also be used for regression tasks, where the objective becomes sensitive. The support vector clustering algorithm, created by Hava Siegelmann and Vladimir Vapnik, applies the statistics of support vectors, developed in the support vector machines algorithm, to categorize unlabeled data. These data sets require unsupervised learning approaches, which attempt to find natural clustering of the data to groups and, then, to map new data according to these clusters. The popularity of SVMs is likely due to their amenability to theoretical
