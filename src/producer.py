# --- IMPORTS ---
import time             # To create delays (sleep) so we don't crash the website
import json             # To format data as JSON string before sending to Kafka
import requests         # The tool that downloads the HTML page (The "Browser")
from bs4 import BeautifulSoup  # The tool that reads HTML and finds text (The "Scraper")
from kafka import KafkaProducer # The tool that connects to our Docker Kafka

# --- CONFIGURATION ---
KAFKA_TOPIC = "news_stream"
KAFKA_SERVER = "localhost:29092" # Since we are running this script ON the VM, we hit localhost
URL = "https://news.ycombinator.com/newest" # The target website (Hacker News - Newest)

def get_kafka_producer():
    """
    Creates the connection to Kafka.
    If Kafka is not ready yet, it waits 5 seconds and tries again.
    """
    producer = None
    while producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                # Kafka only accepts Bytes, so we must encode our JSON string to UTF-8 bytes
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            print("Successfully connected to Kafka!")
        except Exception as e:
            print(f"Waiting for Kafka... Error: {e}")
            time.sleep(5)
    return producer

def scrape_headlines():
    """
    Downloads the website and extracts titles.
    Returns a list of dictionaries: [{'title': '...', 'link': '...'}]
    """
    try:
        # 1. Download the raw HTML code of the website
        response = requests.get(URL)
        
        # 2. Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 3. Find all elements with class 'titleline' (Hacker News specific tag)
        links = soup.select(".titleline > a")
        
        results = []
        for link in links:
            # Create a clean dictionary for each article
            article = {
                "title": link.get_text(),
                "link": link.get("href"),
                "timestamp": time.time() # Add current time for tracking
            }
            results.append(article)
        
        return results
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Starting the News Scraper Producer...")
    
    # 1. Connect to Kafka
    producer = get_kafka_producer()
    
    # 2. Infinite Loop (Run forever until we stop it)
    while True:
        print("Scraping new headlines...")
        
        # 3. Get Data
        articles = scrape_headlines()
        
        # 4. Send Data to Kafka
        for article in articles:
            # We verify the title is not empty
            if article['title']:
                print(f"Sending: {article['title'][:30]}...") # Print first 30 chars
                producer.send(KAFKA_TOPIC, value=article)
        
        # 5. Flush (Force send)
        producer.flush()
        
        # 6. Wait 60 seconds before checking for new news
        print("Sleeping for 60 seconds...")
        time.sleep(60)