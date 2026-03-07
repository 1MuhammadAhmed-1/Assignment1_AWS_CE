from flask import Flask, render_template
import boto3
import json

app = Flask(__name__)
s3 = boto3.client('s3', region_name='us-east-1')
BUCKET_NAME = 'unievent-storage-ahmed-2026'

@app.route('/')
def index():
    try:
        # 1. Pull the JSON file from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key='events.json')
        events_data = json.loads(response['Body'].read())

        # 2. Safely get the list of events
        # .get() prevents crashes if '_embedded' is missing
        events = events_data.get('_embedded', {}).get('events', [])

        print(f"Successfully loaded {len(events)} events from S3.")
        return render_template('index.html', events=events)

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return f"Error loading events: {str(e)}"
    
if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) so the Load Balancer can reach it
    app.run(host='0.0.0.0', port=80)