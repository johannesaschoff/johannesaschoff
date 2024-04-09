import streamlit as st
import requests
import json
import base64

# Securely load your GitHub token from Streamlit secrets
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Assuming 'johannesaschoff' is both your username and the repository name
# Update 'repo' if your repository name is different
repo = "johannesaschoff"
file_path = "game_data.json"  # Path to your file within the repository
branch = "main"

def get_api_url():
    # Correctly format the API URL
    return f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"

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

import streamlit as st

# Assuming the rest of your setup is as previously defined...

def app():
    st.title("Golf Betting Game")
    
    # Fetch the current game data from GitHub
    game_data, sha = read_game_data()
    if not game_data:
        st.stop()

    # Display current round and scores
    st.write(f"Current Round: {game_data['current_round']}")
    st.write("Scores:", game_data['scores'])

    # If the game is over, display the winner and stop
    if game_data['current_round'] > 4:
        winner = max(game_data['scores'], key=game_data['scores'].get)
        st.header(f"Game Over - Winner: {winner}")
        return

    # Allow each user to select a golfer
    for user in ["User 1", "User 2"]:
        game_data['selections'][user] = st.selectbox(f"{user}, select your golfer:",
                                                     ['Golfer 1', 'Golfer 2', 'Golfer 3', 'Golfer 4', 'Golfer 5'],
                                                     key=user)

    # Lock in selections and update GitHub
    if st.button("Lock in Selections"):
        update_game_data(game_data, sha)

    # Manually set the round winner and update scores
    if st.button("Set Round Winner"):
        winner = st.radio("Who won the round?", ["User 1", "User 2"])
        if winner:
            game_data['scores'][winner] += 1
            game_data['current_round'] += 1
            update_game_data(game_data, sha)
            st.success(f"{winner} wins Round {game_data['current_round'] - 1}!")

if __name__ == "__main__":
    app()

if __name__ == "__main__":
    app()
