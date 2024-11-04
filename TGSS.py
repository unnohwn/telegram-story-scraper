def display_ascii_art():
    WHITE = "\033[97m"
    RESET = "\033[0m"
    
    art = r"""


____________________   _________ _________
\__    ___/\_   ___ \ /   _____//   _____/
  |    |   /    \  \/ \_____  \ \_____  \ 
  |    |   \     \____/        \/        \
  |____|    \______  /_______  /_______  /
                   \/        \/        \/
    """
    
    print(WHITE + art + RESET)

display_ascii_art()

from telethon import TelegramClient
from telethon.tl.functions.stories import GetAllStoriesRequest
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import sqlite3
import openpyxl
import os
import schedule
import time
from datetime import datetime, timedelta
import json

db_file = 'stories.db'
excel_file_path = 'stories_info.xlsx'
credentials_file = 'credentials.json'

def prompt_for_credentials():
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")
    phone_number = input("Enter your phone number: ")
    credentials = {
        'api_id': api_id,
        'api_hash': api_hash,
        'phone_number': phone_number
    }
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f)
    return credentials

def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            return json.load(f)
    else:
        return prompt_for_credentials()

credentials = load_credentials()
client = TelegramClient('session_name', credentials['api_id'], credentials['api_hash'])

def prompt_for_interval():
    try:
        interval = int(input("Enter the checking interval in seconds (default is 60 seconds): ") or "60")
    except ValueError:
        print("Invalid input. Using default interval of 60 seconds.")
        interval = 60
    return interval

interval = prompt_for_interval()

def initialize_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stories (
        user_id INTEGER,
        story_id INTEGER PRIMARY KEY,
        timestamp TEXT,
        filename TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_story(user_id, story_id, timestamp, filename):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO stories (user_id, story_id, timestamp, filename)
    VALUES (?, ?, ?, ?)
    ''', (user_id, story_id, timestamp, filename))
    conn.commit()
    conn.close()

def fetch_stories_from_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, story_id FROM stories')
    stories = cursor.fetchall()
    conn.close()
    return set(stories)

def export_to_excel():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stories')
    stories = cursor.fetchall()
    conn.close()

    if not os.path.exists(excel_file_path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Stories"
        ws.append(["User ID", "Story ID", "Timestamp", "Filename"])
        wb.save(excel_file_path)

    wb = openpyxl.load_workbook(excel_file_path)
    ws = wb.active

    existing_ids = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        user_id, story_id, _, _ = row
        existing_ids.add((user_id, story_id))

    for story in stories:
        user_id, story_id, timestamp, filename = story
        if (user_id, story_id) not in existing_ids:
            ws.append([user_id, story_id, timestamp, filename])

    wb.save(excel_file_path)

async def scrape_stories():
    await client.start(phone=credentials['phone_number'])
    
    try:
        all_stories = await client(GetAllStoriesRequest())

        if not all_stories or not all_stories.peer_stories:
            return

        existing_stories_in_db = fetch_stories_from_db()
        new_stories_count = 0

        for peer_story in all_stories.peer_stories:
            user_id = peer_story.peer.user_id
            stories = peer_story.stories

            for story in stories:
                story_id = story.id
                
                if (user_id, story_id) in existing_stories_in_db:
                    continue

                media = story.media
                timestamp_utc = story.date
                timestamp_swedish = timestamp_utc + timedelta(hours=2)
                timestamp = timestamp_swedish.strftime('%Y-%m-%d %H:%M:%S')
                
                filename = None

                try:
                    if isinstance(media, MessageMediaPhoto):
                        photo = media.photo
                        filename = f"{user_id}_{story_id}.jpg"
                        await client.download_media(photo, file=filename)

                    elif isinstance(media, MessageMediaDocument):
                        document = media.document
                        filename = f"{user_id}_{story_id}.{document.mime_type.split('/')[1]}"
                        await client.download_media(document, file=filename)

                    if filename:
                        insert_story(user_id, story_id, timestamp, filename)
                        new_stories_count += 1

                except Exception as e:
                    print(f"Failed to download media for story {story_id}: {e}")

        if new_stories_count > 0:
            print(f"Detected and saved {new_stories_count} new stories.")
        
    except Exception as e:
        print(f"Failed to scrape stories: {str(e)}")

    await client.disconnect()

def job():
    print(f"Checking for new stories at {datetime.now()}")
    client.loop.run_until_complete(scrape_stories())
    export_to_excel()

initialize_database()

print("Running initial check for stories...")
client.loop.run_until_complete(scrape_stories())

print(f"Starting scheduled job with a {interval}-second interval. Press Ctrl+C to exit.")
schedule.every(interval).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
