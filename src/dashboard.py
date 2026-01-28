import streamlit as st
import pymongo
import pandas as pd
import time

# --- CONFIGURATION ---
# We use 'localhost' because this runs on the VM, talking to the mapped port 27017
MONGO_URI = "mongodb://admin:password@localhost:27017/"
DB_NAME = "news_db"
COLLECTION_NAME = "headlines"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Real-Time AI News Monitor",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Real-Time AI News Sentiment Pipeline")
st.markdown("""
This dashboard monitors **Hacker News** in real-time.
- **Data Pipeline:** Kafka -> Spark Streaming -> MongoDB
- **AI Model:** TextBlob (Sentiment Analysis)
""")

# --- CONNECT TO DATABASE ---
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(MONGO_URI)

try:
    client = init_connection()
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Check connection
    client.server_info()
except Exception as e:
    st.error(f"Could not connect to MongoDB. Error: {e}")
    st.stop()

# --- LIVE METRICS ---
placeholder = st.empty()

while True:
    with placeholder.container():
        # 1. Fetch latest 50 records from MongoDB
        # sort([('_id', -1)]) means "Give me the newest data first"
        data = list(collection.find().sort([('_id', -1)]).limit(50))
        
        if data:
            df = pd.DataFrame(data)
            
            # KPI Cards
            kpi1, kpi2, kpi3 = st.columns(3)
            
            # Total Count
            total_count = collection.count_documents({})
            kpi1.metric("Total Articles Scraped", total_count)
            
            # Average Sentiment
            avg_sentiment = df['sentiment_score'].mean()
            # Color logic for sentiment
            sentiment_color = "normal"
            if avg_sentiment > 0.1: sentiment_color = "off" # Greenish (Streamlit default)
            elif avg_sentiment < -0.1: sentiment_color = "inverse" # Reddish
            
            kpi2.metric("Avg Sentiment (Last 50)", f"{avg_sentiment:.4f}")
            
            # Latest Headline
            latest_news = df.iloc[0]['title']
            kpi3.metric("Latest Headline", latest_news[:40] + "...")

            # 2. Charts & Data
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Sentiment Trend")
                # We reverse the dataframe so the chart goes Left(Old) -> Right(New)
                st.line_chart(df.iloc[::-1], x='title', y='sentiment_score')

            with col2:
                st.subheader("Latest Raw Data")
                st.dataframe(df[['title', 'sentiment_score']].head(10), hide_index=True)
        else:
            st.info("Waiting for data stream... (Check if Producer/Processor are running)")

        # Refresh every 2 seconds
        time.sleep(2)