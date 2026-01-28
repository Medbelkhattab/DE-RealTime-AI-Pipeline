# Real-Time AI News Pipeline

An End-to-End Data Engineering project that scrapes Hacker News, processes sentiment in real-time using Apache Spark, and visualizes trends.

##  Architecture
![Architecture Diagram]((https://mermaid.ink/img/pako:eNqVVs1u20YQfpUFgxQyYMmkJJoi2xiQJTpWbEuqKNlNoiBYUUuREMVVlmQcN84hbY8tmiaH9tae2qKnAr0U6Nv0BdpH6CyXP9ZPXIQn7i7nm5lv5pvlS8mmUyIZ0ozhpYuG7XGA4Ll7F5XLZWQNH56aFn8V27aPw7BNHOTjZUSXyPF837hDFEd1yG4YMTonxh1ZUTV9ki7Ll940co3q8sWuTX3KjImP7fnHa3BeEBEWkCgFdBynRuQckOyriix_EKBLwxysRlRHzcHqWKk37E2wdGOKQxczhq8MpCL1NhdTas8JyyhoOCrRcyfKRCXVtYjrt0ccEvbcs0nBADw5Xq1WWwVTtoKt1E6poN5oaHXaJrroDU7bRRXDeCKqnZ0_Hkv__vj1GzQ8NldtxtITYcKf42brxBw87ZoXVokbvPsdHeOEgy65DNEFmYReRMbSjmEYWUEL69Nmf9jrJ4Zv_0IPe6NBuvXJhO0dlM69MMY-OifMczwbRx4NdgSUaDUBRILpOFjJslpBzUejgYnOz9BxzxpuyTI5fwrnkObfP7z-589v10xKo0kcRPHOSrZTjxGbh4GGh8Vu8ZbD9we99qgFxDT7fcHkuy9QyOy9JaPT2CassrxaQU7Y6N3vtICM_lXkgotTOvNsI2HCsgGVoI-QxZNNGEhbo0BIaNgMKaWkVkHtHi8V6ppDKONJwclK4OIjqOdQhP3mj3U7qAqLeFnaOMKoRXhRdzZyWV1BEFbayl2YLOHq6aNe73HSAz-_5u8nptk3B6IDznCAZwn-zpNtSfPnpHl00hQA734VK2E8dAk6jB3nf-xXV2dNa2gOBNwvPyGr34ScxeYNVBqGt2JypjKUt7-lKGKzQOkzapMwpB8UXqfbSdn6_ivetckGKlm1nQK4yWzXe05uhT3rde-nQN98KVbtQwExINgvD70FQe3DWzHMz_oD07IEyneJiBKg7EDAtQ_RqPNenLxtN2XMJ8_Rae8CWeanI7PbMkXP5t9YEVkixUCJOrxgJg5uTCR07x4aSzDz7kM7D8izmIRRGhO9DHyKp-h4eHYKscGXB0J_a0Mz8VE1UCeYgTFXfumYXyMRRS0aRNgLeHcFuXyFSxhA_Th00QOr1010ktaGIp_a2OcXkVHVZb2auU66dpvrGnftMAyDPrajmBEkJLEA3YkvQTGoXCkfXIPExRk65JcCS3x2kpmLfQNVlYZyfdORaGphW4eJGYbeDAYbDufhmqkma9p12r7bgqwbWS9DFVApJ2YbS0kAgiW1AkWBGlgRI3ghKDpidIHm2Jlj4yY_7_etQv0jynjapQvmRTyCAQljPwpTj8JWuNyvIP4RaA8zaIcor8vCCzwKLmU5c5kIaxNByxDa1A4LcxrM6HRiVDVZ0XIEroVtMe_zogpyQRqcokBcK-lgFCJKCtOooCMS2W7RRTcqyp1dZ2JbF4ZmoBGoDZ3RwAOCkso8pDG6xAAHq6xrk_sWlAW56RV07pFL9IBOAANHcZqgG0VLY2-v0zcaciMhqFw-SPtnE0WRK6jlEnuOjjyfbEAAx0oOUXC8gqBkCIV2VmLIATZzby6X_hVEf-Vn10x21cP04cITm8U9B9vir03ahf9dbyoZIDWyKy0IW2C-lF5yk7EUuaC6sWTA6xSz-VgaB6_AZomDR5QuMjNG45krGQ72Q1jFyymOSNvDcLsu8l0Gs46wFoUfDMlQEwjJeCm9gIWsV_R9tSHrtZpWryvarnQlGYpW0apaTa3LugZ7jfqrXenzxKdcaei1hq7ouqw06lqjpr_6D1rHfE4))

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
