import requests
import boto3
import json
from datetime import datetime

def fetch_university_events():
    # --- CONFIGURATION ---
    # Replace these two with your actual values!
    API_KEY = "TVSPiIw88ZzvlDdnIXT0i8L9t7GxmpTw"
    BUCKET_NAME = 'unievent-storage-ahmed-2026'
    # ---------------------

    url = f"https://app.ticketmaster.com/discovery/v2/events.json?keyword=university&apikey={API_KEY}"
    
    print("Connecting to Ticketmaster API...")
    
    try:
        # This is the line that was likely missing or broken:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            file_name = f"events_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            
            print(f"Uploading to S3 bucket: {BUCKET_NAME}")
            s3 = boto3.client('s3')
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"data/{file_name}",
                Body=json.dumps(data, indent=4),
                ContentType='application/json'
            )
            print("--- SUCCESS ---")
            print(f"File saved in S3 as: data/{file_name}")
        else:
            print(f"API Error! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_university_events()