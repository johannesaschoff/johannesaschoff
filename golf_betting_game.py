import streamlit as st
import requests
import json
import base64
import os

# Securely load your GitHub token from an environment variable
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Correct repository and file path details
repo = "johannesaschoff/johannesaschoff"  # GitHub username or organization
file_path = "game_data.json"  # Path to your file within the repository
branch = "main"

def get_api_url():
    return f"https://api.github.com/repos/{repo}/{repo}/contents/{file_path}?ref={branch}"

# Function to read game data from GitHub
def read_game_data():
    response = requests.get(get_api_url(), headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        content = base64.b64decode(response_json['content']).decode('utf-8')
        return json.loads(content), response_json['sha']
    else:
        st.error(f"Failed to fetch game data: {response.json()}")
        return {}, ""

# Function to update game data on GitHub
def update_game_data(data, sha):
    update_data = {
        "message": "Update game data",
        "content": base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8'),
        "branch": branch,
        "sha": sha
    }
    response = requests.put(get_api_url(), headers=headers, data=json.dumps(update_data))
    if response.status_code == 200:
        st.success("Game data updated successfully!")
    else:
        st.error(f"Failed to update game data: {response.json()}")

# Example usage within Streamlit
def app():
    st.title("Golf Betting Game")
    
    game_data, sha = read_game_data()
    if not game_data:
        st.stop()

    # Example of displaying and updating game data
    # Add your game logic here

if __name__ == "__main__":
    app()
