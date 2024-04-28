from flask import Flask, jsonify
import requests
import pandas as pd

app = Flask(__name__)

TODOIST_API_URL = "https://api.todoist.com/rest/v2/tasks"
TODOIST_TOKEN = "3d9b1ee0d8f344734b1c0de3c6c1443326f209df"  # Replace with your Todoist API token

@app.route('/onething', methods=['GET'])
def get_one_thing():
    headers = {
        "Authorization": f"Bearer {TODOIST_TOKEN}"
    }
    params = {
        "filter": "@exo | ((#BNYM | @work) & (((p1 | p2) & (no due date)) | (today | overdue) | (7 days & @deadline) | (/Todo)))"
    }

    response = requests.get(TODOIST_API_URL, headers=headers, params=params)
    tasks = response.json()

    # Return the title of the highest priority task
    if tasks:
        df = pd.json_normalize(tasks)
        result = df.sort_values( 
                    by=['priority', 'due.date', 'created_at'], 
                    ascending= [False,  True, True])['content'].head(1).to_string(index=False)
        return result
    else:
        return "No tasks found."

if __name__ == '__main__':
    app.run(debug=True)

