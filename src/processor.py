import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, lower
from pyspark.sql.types import StructType, StringType, FloatType, DoubleType
from textblob import TextBlob

# --- CONFIGURATION ---
KAFKA_TOPIC = "news_stream"
KAFKA_SERVER = "localhost:29092"

# MINIO CONFIG
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# MONGODB CONFIG
# FIX: Changed 'mongodb' to 'localhost' so the VM can find the container
MONGO_URI = "mongodb://admin:password@localhost:27017/?authSource=admin"

def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0.0

sentiment_udf = udf(get_sentiment, FloatType())

# --- THE DUAL WRITER FUNCTION ---
def write_to_mongo_and_minio(df, epoch_id):
    # 1. Write to MinIO (Historical Storage)
    df.write \
        .format("parquet") \
        .mode("append") \
        .save("s3a://news-data/raw/")
    
    # 2. Write to MongoDB (Real-Time Dashboard)
    df.write \
        .format("mongodb") \
        .mode("append") \
        .option("connection.uri", MONGO_URI) \
        .option("database", "news_db") \
        .option("collection", "headlines") \
        .save()
    
    pass

if __name__ == "__main__":
    # 1. INITIALIZE SPARK
    spark = SparkSession.builder \
        .appName("RealTimePipeline") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.apache.hadoop:hadoop-aws:3.3.2,org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT) \
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # 2. SCHEMA
    schema = StructType() \
        .add("title", StringType()) \
        .add("link", StringType()) \
        .add("timestamp", DoubleType())

    # 3. READ STREAM
    print("Reading from Kafka...")
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_SERVER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    # 4. PROCESS
    processed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("clean_title", lower(col("title"))) \
        .withColumn("sentiment_score", sentiment_udf(col("clean_title")))

    # 5. WRITE STREAM
    print("Streaming to MinIO (Lake) and MongoDB (App)...")
    
    query = processed_stream.writeStream \
        .foreachBatch(write_to_mongo_and_minio) \
        .option("checkpointLocation", "s3a://news-data/checkpoints/") \
        .start()

    query.awaitTermination()