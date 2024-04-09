import streamlit as st
import requests
import json
import base64

# GitHub API headers with your personal access token
headers = {
    "Authorization": "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",
    "Accept": "application/vnd.github.v3+json"
}

# GitHub repository and file details
repo = "johannesaschoff/johannesaschoff"
file_path = "johannesaschoff/game_data.json"
branch = "main"

# Utility function to get the full path for the API URL
def get_api_url():
    return f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"

# Read game data from GitHub
def read_game_data():
    response = requests.get(get_api_url(), headers=headers)
    response_json = response.json()
    content = base64.b64decode(response_json['content']).decode('utf-8')
    return json.loads(content), response_json['sha']

# Update game data on GitHub
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
        st.error("Failed to update game data.")

# Streamlit app layout
def app():
    game_data, sha = read_game_data()

    st.title("Golf Betting Game")

    # Display current round and scores
    st.header(f"Round {game_data['current_round']}")
    st.write("Scores:", game_data['scores'])

    # Let users select golfers
    for user in ["User 1", "User 2"]:
        game_data['selections'][user] = st.selectbox(f"{user}, select your golfer:", ['Golfer 1', 'Golfer 2', 'Golfer 3', 'Golfer 4', 'Golfer 5'], key=user)

    if st.button('Lock in Selections'):
        update_game_data(game_data, sha)

# Run the app
if __name__ == "__main__":
    app()
