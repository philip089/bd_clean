from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
import sys

def create_spark_session():
    try:
        spark = SparkSession.builder \
            .appName("HadoopConnectorWithErrorHandling") \
            .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
            .config("spark.yarn.resourcemanager.address", "yarn:8032") \
            .config("spark.executor.instances", "2") \
            .config("spark.executor.memory", "1g") \
            .config("spark.executor.cores", "1") \
            .config("spark.driver.memory", "1g") \
            .getOrCreate()
        return spark
    except Exception as e:
        print(f"Failed to create Spark session: {e}", file=sys.stderr)
        sys.exit(1)

def read_data_from_hdfs(spark, file_path):
    try:
        df = spark.read.text(file_path)
        df.show()
        print(file_path)
    except AnalysisException as e:
        print(f"File read error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    spark_session = create_spark_session()
    if spark_session:
        read_data_from_hdfs(spark_session, "hdfs://namenode:9000/scraperdata/dataytube/DE.csv")
        spark_session.stop()