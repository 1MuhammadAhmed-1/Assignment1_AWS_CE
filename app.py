from flask import Flask, render_template
import boto3
import json

app = Flask(__name__)
s3 = boto3.client('s3', region_name='us-east-1') # Change region if needed
BUCKET_NAME = 'unievent-storage-ahmed-2026'

@app.route('/')
def index():
    try:
        # Pull the JSON file your other script created
        response = s3.get_object(Bucket=BUCKET_NAME, Key='events.json')
        events_data = json.loads(response['Body'].read())
        # Ticketmaster data is usually nested under _embedded
        events = events_data.get('_embedded', {}).get('events', [])
        return render_template('index.html', events=events)
    except Exception as e:
        return f"Error loading events: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)