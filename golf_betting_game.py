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

# Repository and file path details
repo = "johannesaschoff/johannesaschoff"  # Assuming this is both your GitHub username and repo name
file_path = "game_data.json"  # Path to your file within the repository
branch = "main"

def get_api_url():
    """Correctly format the GitHub API URL."""
    return f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"

def read_game_data():
    """Function to read game data from GitHub."""
    response = requests.get(get_api_url(), headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        content = base64.b64decode(response_json['content']).decode('utf-8')
        return json.loads(content), response_json['sha']
    else:
        st.error(f"Failed to fetch game data: {response.json()}")
        return {}, ""

def update_game_data(data, sha):
    """Function to update game data on GitHub."""
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


def display_leaderboard(scores, container):
    # Sort the scores in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Add the leaderboard header
    container.markdown("## Leaderboard")
    
    # Add each user and their score to the leaderboard
    for index, (user, score) in enumerate(sorted_scores):
        # Use HTML for custom alignment and styling
        if index == 0:  # Leader gets a crown to the left of their name
            container.markdown(f"""
                <div style="display:flex;align-items:center;">
                    <span style="color:gold;">&#x1F451;&nbsp;</span>
                    <span style="font-weight:bold;">{user}:</span>
                    <span>&nbsp;{score} points</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            container.markdown(f"""
                <div style="display:flex;align-items:center;">
                    <span style="font-weight:bold;">{user}:</span>
                    <span>&nbsp;{score} points</span>
                </div>
                """, unsafe_allow_html=True)


def app():
    st.title("Golf Betting Game")
    
    # Layout with 2 columns: Left for selections, right for leaderboard
    col1, col2 = st.columns([3, 1])
    
    # Adjust the game data as per your actual game's data structure
    game_data = {
        "scores": {"User 1": 5, "User 2": 3}  # Adjusted to two users for this example
    }
    
    with col1:
        st.subheader("Select Your Golfer")
        # Example selection box for each user
        for user in game_data['scores'].keys():
            st.selectbox(f"{user}, select your golfer:",
                         ['Golfer 1', 'Golfer 2', 'Golfer 3', 'Golfer 4', 'Golfer 5'],
                         key=user)
    
    with col2:
        display_leaderboard(game_data['scores'], col2)

if __name__ == "__main__":
    app()
