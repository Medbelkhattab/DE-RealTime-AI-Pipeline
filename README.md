# Real-Time AI News Pipeline

An End-to-End Data Engineering project that scrapes Hacker News, processes sentiment in real-time using Apache Spark, and visualizes trends.

##  Architecture
![Architecture Diagram](https://mermaid.ink/img/pako:eNp1U9tu2zAM_RXBz...COPY_YOUR_MERMAID_LINK_HERE...)

## Tech Stack
- **Ingestion:** Python (BeautifulSoup), Apache Kafka, Zookeeper
- **Processing:** Apache Spark (Structured Streaming), TextBlob (Sentiment Analysis)
- **Storage:** MinIO (Data Lake/Parquet), MongoDB (NoSQL)
- **Visualization:** Streamlit (Real-time Dashboard), Mongo Express

## How it Works
1. **Producer:** Scrapes `news.ycombinator.com` every 60 seconds.
2. **Kafka:** Buffers the data into the `news_stream` topic.
3. **Spark:** Reads the stream, cleans text, calculates sentiment polarity (-1 to 1).
4. **Storage:**
   - Raw data -> MinIO (Parquet) for historical analysis.
   - Processed data -> MongoDB for real-time application.
5. **Dashboard:** Streamlit queries MongoDB to display live trends.

##  Project Structure
- `src/producer.py`: Kafka Producer logic.
- `src/processor.py`: Spark Streaming & Dual-Write logic.
- `src/dashboard.py`: Streamlit Frontend.
- `docker-compose.yaml`: Infrastructure as Code (IaaC).
