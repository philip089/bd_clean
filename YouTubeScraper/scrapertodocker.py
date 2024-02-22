
import docker
import paramiko
import os
import time

def start_hadoop_container(hadoop_image):
    client = docker.from_env()
    hadoop_container = client.containers.run(hadoop_image, detach=True, tty=True, name='hdfs-datanode1')
    return hadoop_container

def copy_data_to_hadoop_container(local_data_path, hadoop_container, remote_path='/scraperdata'):
    client = docker.from_env()

    # Copy data to Hadoop container
    local_data = os.path.basename(local_data_path)
    client.containers.get(hadoop_container.id).put_archive(os.path.dirname(local_data_path), remote_path)

    return os.path.join(remote_path, local_data)

def execute_hadoop_command(hadoop_container, command):
    client = docker.from_env()
    exec_id = client.containers.get(hadoop_container.id).exec_run(command, tty=True)
    return exec_id

def main():
    # Docker image for Hadoop
    hadoop_image = 'your-hadoop-image'

    # Local data path in the container
    local_data_path = '/scraper/data'

    # Start Hadoop container
    hadoop_container = start_hadoop_container(hadoop_image)

    # Wait for Hadoop services to be ready (adjust the wait time based on your setup)
    time.sleep(30)

    # Copy data to Hadoop container
    remote_data_path = copy_data_to_hadoop_container(local_data_path, hadoop_container)

    # Execute Hadoop command to import data
    hadoop_command = f'hdfs dfs -copyFromLocal {remote_data_path} /scraper/'
    execute_hadoop_command(hadoop_container, ['bash', '-c', hadoop_command])

    # Verify data in HDFS
    execute_hadoop_command(hadoop_container, ['hdfs', 'dfs', '-ls', '/scraper/'])

if __name__ == "__main__":
    main()

