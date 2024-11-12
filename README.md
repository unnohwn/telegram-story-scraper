# Telegram Story Scraper 📱

A Python script that allows you to automatically scrape and download stories from your Telegram friends using the Telethon library. The script continuously monitors and saves both photos and videos from stories, along with their metadata.

<div align="left">
  <img src="Screenshot TGSS.png" alt="Telegram Story Scraper Interface" width="800"/>
  <p><i>TGSS - Main Interface</i></p>
</div>

## Important Note About Story Access ⚠️

Due to Telegram API restrictions, this script can only access stories from:
- Users you have added to your friend list
- Users whose privacy settings allow you to view their stories

This is a limitation of Telegram's API and cannot be bypassed.

## Features 🚀

- Automatically scrapes all available stories from your Telegram friends
- Downloads both photos and videos from stories
- Stores metadata in SQLite database
- Exports data to Excel spreadsheet
- Real-time monitoring with customizable intervals
- Timestamp is set to (UTC+2)
- Maintains record of previously downloaded stories
- Resume capability
- Automatic retry mechanism

## Prerequisites 📋

Before running the script, you'll need:

- Python 3.7 or higher
- Telegram account
- API credentials from Telegram
- Friends on Telegram whose stories you want to track

### Required Python packages

```
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
telethon
openpyxl
schedule
```

## Getting Telegram API Credentials 🔑

1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Click on "API development tools"
4. Fill in the form:
   - App title: Your app name
   - Short name: Your app short name
   - Platform: Can be left as "Desktop"
   - Description: Brief description of your app
5. Click "Create application"
6. You'll receive:
   - `api_id`: A number
   - `api_hash`: A string of letters and numbers
   
Keep these credentials safe, you'll need them to run the script!

## Setup and Running 🔧

1. Clone the repository:
```bash
git clone https://github.com/unnohwn/telegram-story-scraper.git
cd telegram-story-scraper
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python TGSS.py
```

4. On first run, you'll be prompted to enter:
   - Your API ID
   - Your API Hash
   - Your phone number (with country code)
   - Verification code (sent to your Telegram)
   - Checking interval in seconds (default is 60)

## How It Works 🔄

The script:
1. Connects to your Telegram account
2. Periodically checks for new stories from your friends
3. Downloads any new stories (photos/videos)
4. Stores metadata in a SQLite database
5. Exports information to an Excel file
6. Runs continuously until interrupted (Ctrl+C)

## Data Storage 💾

### Database Structure (stories.db)

SQLite database containing:
- `user_id`: Telegram user ID of the story creator
- `story_id`: Unique story identifier
- `timestamp`: When the story was posted (UTC+2)
- `filename`: Local filename of the downloaded media

### CSV and Excel Export (stories_export.csv/xlsx)

Export file containing the same information as the database, useful for:
- Easy viewing of story metadata
- Filtering and sorting
- Data analysis
- Sharing data with others

### Media Storage 📁

- Photos are saved as: `{user_id}_{story_id}.jpg`
- Videos are saved with their original extension: `{user_id}_{story_id}.{extension}`
- All media files are saved in the script's directory

## Features in Detail 🔍

### Continuous Monitoring

- Customizable checking interval (default: 60 seconds)
- Runs continuously until manually stopped
- Maintains state between runs
- Avoids duplicate downloads

### Media Handling

- Supports both photos and videos
- Automatically detects media type
- Preserves original quality
- Generates unique filenames

## Error Handling 🛠️

The script includes:
- Automatic retry mechanism for failed downloads
- Error logging for failed operations
- Connection error handling
- State preservation in case of interruption

## Limitations ⚠️

- Subject to Telegram's rate limits
- Stories must be currently active (not expired)
- Media download size limits apply as per Telegram's restrictions

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer ⚖️

This tool is for educational purposes only. Make sure to:
- Respect Telegram's Terms of Service
- Obtain necessary permissions before scraping
- Use responsibly and ethically
- Comply with data protection regulations
- Respect user privacy
