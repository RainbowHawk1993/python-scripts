import asyncio
import aiohttp
import sqlite3
import csv
import logging
import time

logging.basicConfig(filename='api_fetch.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

API_URL = "https://jsonplaceholder.typicode.com/posts"
DATABASE_FILE = "posts.db"
CSV_FILE = "posts.csv"

async def fetch_data(session, url):
    start_time = time.time()
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                end_time = time.time()
                logging.info(f"Successfully fetched data from {url} in {end_time - start_time:.2f} seconds")
                return data
            else:
                end_time = time.time()
                error_message = f"Error fetching data from {url}: Status code {response.status}"
                logging.error(error_message)
                return None
    except aiohttp.ClientError as e:
        end_time = time.time()
        error_message = f"Client error fetching {url}: {e}"
        logging.error(error_message)
        return None
    except asyncio.TimeoutError:
        end_time = time.time()
        error_message = f"Timeout fetching {url}"
        logging.error(error_message)
        return None


async def fetch_all_data(urls):
    async with aiohttp.ClientSession() as session:
       tasks = [fetch_data(session, url) for url in urls]
       results = await asyncio.gather(*tasks)
       return results


def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_database(data):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    for post in data:
        if post:
            try:
                cursor.execute("INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)",
                               (post['id'], post['userId'], post['title'], post['body']))
            except sqlite3.IntegrityError:
                logging.warning(f"Duplicate ID {post['id']} encountered. Skipping.")
            except Exception as e:
                logging.error(f"Error inserting data into database: {e}")
    conn.commit()
    conn.close()

def save_to_csv(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'user_id', 'title', 'body'])
        for post in data:
             if post:
                writer.writerow([post['id'], post['userId'], post['title'], post['body']])

async def main():
    create_database()
    urls = [f"{API_URL}/{i}" for i in range(1, 101)]
    posts_data = await fetch_all_data(urls)
    save_to_database(posts_data)
    save_to_csv(posts_data)
    print(f"Data fetched and saved to {DATABASE_FILE} and {CSV_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
