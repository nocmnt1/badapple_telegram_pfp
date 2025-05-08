from telethon.sync import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.errors import FloodWaitError
import os
import time
import re

# Your Telegram API credentials
api_id = '' 
api_hash = ''
phone_number = ''

# Path to the frames folder
frames_folder = ''

def upload_profile_photo(client, photo_path, max_retries=5):
    for attempt in range(max_retries):
        try:
            file = client.upload_file(photo_path)
            client(UploadProfilePhotoRequest(file=file))
            return True
        except FloodWaitError as e:
            wait_time = e.seconds
            print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
        except Exception as e:
            error_message = str(e)
            wait_match = re.search(r"A wait of (\d+) seconds is required", error_message)
            if wait_match:
                wait_time = int(wait_match.group(1))
                print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print(f"Error: {error_message}")
                return False
    
    print(f"Failed to upload after {max_retries} attempts.")
    return False

# Create and connect the client
with TelegramClient('session_name', api_id, api_hash) as client:
    # Authorization
    client.start(phone=phone_number)

    n = int(input("Enter the number of frames to upload: "))
    
    for i in range(1, n + 1):
        photo_path = os.path.join(frames_folder, f"{i}.jpg")
        
        if os.path.exists(photo_path):
            print(f"Uploading frame {i}...")
            if upload_profile_photo(client, photo_path):
                print(f"Successfully uploaded frame {i}")
            else:
                print(f"Failed to upload frame {i}")
            
            # Add a small delay between uploads to avoid hitting rate limits too frequently
            time.sleep(5)
        else:
            print(f"Frame {i} not found")

    print("Profile picture update process completed!")
