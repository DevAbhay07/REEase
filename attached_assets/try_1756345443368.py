import json
from pprint import pprint

# Read the input JSON file
with open("text-summarizer/abc.json") as f:
    data = json.load(f)

# Create a dictionary to store body texts for each thread_id
thread_data = {}

# Iterate over each message and organize by thread_id
for message in data:
    thread_id = message['thread_id']
    body_text = message['body']

    if thread_id not in thread_data:
        thread_data[thread_id] = []

    thread_data[thread_id].append(body_text)

# Create a list of dictionaries with thread_id and body texts
output_data = []
for thread_id, body_texts in thread_data.items():
    output_data.append({
        "thread_id": thread_id,
        "body": body_texts
         
    })

# Print the output data
print(output_data)
