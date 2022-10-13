# Lab 2 - Convert WordCount to UrlCount

In this lab, we took WordCount (an existing Hadoop application that is extensively described in the [Hadoop tutorial](https://hadoop.apache.org/docs/r3.0.3/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)) and modified it into UrlCount. Instead of using classic Java approach, I used the [Hadoop streaming API](https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/) to implement the lab in Python.

Before starting with the lab, I went through `Dataproc` Qwiklabs tutorial to understand and get familiar with how to create cluster with default and different number of working nodes. 

After the completion of  `Dataproc` Qwiklabs tutorial, I had my [https://coding.csel.io](https://coding.csel.io) environment set up to test the provided WordCount program. I  was able to successfuly run the WordCount program on my laptop. Then I modified `WordCount1` program to `URLCount` by altering the Mapper.py file in the directory to count **URLs** from the input files than the **words** and Reducer.py file to keep only the URLs if their **count > 5**. Then I tested the program for URL Count by slightly modifying the **Makefile** to pick URLMapper.py and Reducer.py files in streaming rather than Mapper.py and Reducer.py

I tested my URL Count program using streaming API in local coding environment and I was able to obtain desired result and image uploaded to github as:
*Local run result.PNG*
![Local run result](https://user-images.githubusercontent.com/78228113/132429670-c1d7c094-156a-4bbb-992e-7125c79244f1.PNG)


Using Qwiklabs credentials, I created a cluster with **4 working nodes** and then modified the cluster to have **2 working nodes** and used following commands to execute the program:
`make` to compile and create jar file for streaming.
`make prepare` copies two files from Wikipedia that are used as reference input. Thse files are placed in directory input.
`make stream` to run streaming version of URL Count program. or `time make stream` to run streaming version to also provide the execution time.

For this assignment, I have used the following resources:
+ I have used https://coding.csel.io environment in the local system for initial development and testing.
+ I have used Qwiklabs tutorial to understand the creation and modification of hadoop cluster.
+ I have used GCP Dataproc environment to run my program in Hadoop clusters and to work with variable number of nodes.
+ I have used github to access required material to run the program and update it as required.


While running hadoop cluster in Dataproc environment, I did come across some errors like - `JAR does not exist or is not a normal file` and 'No such file or directory' and so on. With the help of class lecture recordings, piazza discussions, attending office hours with the course instructors and discussions with classmates, I was able to rectify my mistakes and run the URL Count program successfully on the Dataproc environment.

Discussion partners - Sanjeev and Suhas.

The screenshot of result after running the URL Count program in Dataproc environment is uploaded to github as:
*lab2 output from reducers.PNG*
![lab2 output from reducers](https://user-images.githubusercontent.com/78228113/132429710-86c5ce0b-faf9-4ffe-9519-0f44c6d705ff.PNG)


I noticed that execution time for a `Cluster with 4 Working nodes` is slightely less compared to `Cluster with 2 Working nodes`. The execution times are 39.366s and 51.328s respectively for 4 and 2 working nodes. I have also uploaded the screenshots for execution time using 4 and 2 nodes as:

*Dataproc Execution time 4 worker nodes.PNG* 
![Dataproc Execution time 4 worker nodes](https://user-images.githubusercontent.com/78228113/132429734-de792c22-cb64-41e9-834f-c13c38f7222c.PNG)
*Dataproc Execution time 2 worker nodes.PNG*
![Dataproc Execution time 2 worker nodes](https://user-images.githubusercontent.com/78228113/132429748-96a7ed00-9659-4fea-8612-3bfc0b74fb52.PNG)

Explanation for **The Java WordCount implementation used a `Combiner` to improve efficiency, but that may cause problems for this application and produce a different output.**
The Java has inbuilt `Combiner` stage as a part in `Reducer` which when implemented explicitly in URL Count `Mapper` would result in overlapping of combiner stages from Mapper as well as Reducer stages there by duplicating the counts. This leads to the exhibit of wrong output.

