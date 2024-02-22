FROM ubuntu:23.10


####################
# JAVA
####################

ENV JAVA_HOME		/usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-8-jdk && \
    rm -rf /var/lib/apt/lists/*



####################
# HADOOP
####################

ENV HADOOP_VERSION	3.3.6

ENV HADOOP_HOME		/usr/local/hadoop
ENV HADOOP_OPTS		-Djava.library.path=/usr/local/hadoop/lib/native
ENV PATH		$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

ENV YARN_RESOURCEMANAGER_USER root
#ENV HADOOP_SECURE_DN_USER root
ENV YARN_NODEMANAGER_USER root

####### 
# Spark
#########



RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget libzip4 libsnappy1v5 libssl-dev && \
    wget http://archive.apache.org/dist/hadoop/core/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    apt-get remove -y wget && \
    rm -rf /var/lib/apt/lists/* && \
    tar -zxf /hadoop-$HADOOP_VERSION.tar.gz && \
    rm /hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION /usr/local/hadoop && \
    mkdir -p /usr/local/hadoop/logs
    


# Overwrite default HADOOP configuration files with our config files
COPY conf  $HADOOP_HOME/etc/hadoop/


RUN mkdir -p /data/dfs/data /data/dfs/name /data/dfs/namesecondary && \
    hdfs namenode -format
VOLUME /data


# Helper script for starting YARN
ADD start-yarn.sh /usr/local/bin/start-yarn.sh



####################
# PORTS
####################

EXPOSE 9000 9870 9866 9867 9864 9868 8088



CMD ["hdfs"]
