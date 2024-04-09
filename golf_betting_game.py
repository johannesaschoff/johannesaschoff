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


def display_leaderboard(scores):
    # Sort the scores in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Initialize the leaderboard as a Markdown string
    leaderboard_md = "## Leaderboard\n\n"
    
    # Add each user and their score to the leaderboard
    for index, (user, score) in enumerate(sorted_scores):
        # Add a crown icon for the leader
        if index == 0:  # Check if this is the leader
            leaderboard_md += f":crown: **{user}**: {score} points\n\n"
        else:
            leaderboard_md += f"**{user}**: {score} points\n\n"
    
    # Display the leaderboard using Streamlit's Markdown
    st.markdown(leaderboard_md, unsafe_allow_html=True)

def app():
    """Main Streamlit app function."""
    st.title("Golf Betting Game")
    
    game_data, sha = read_game_data()
    if not game_data:
        st.stop()

    st.write(f"Current Round: {game_data['current_round']}")
    st.write("Scores:", game_data['scores'])
    display_leaderboard(game_data['scores'])


    if game_data['current_round'] > 4:
        winner = max(game_data['scores'], key=game_data['scores'].get)
        st.header(f"Game Over - Winner: {winner}")
        return

    for user in ["User 1", "User 2"]:
        game_data['selections'][user] = st.selectbox(f"{user}, select your golfer:",
                                                     ['Golfer 1', 'Golfer 2', 'Golfer 3', 'Golfer 4', 'Golfer 5'], key=user)

    if st.button("Lock in Selections"):
        update_game_data(game_data, sha)

    if st.button("Set Round Winner"):
        winner = st.radio("Who won the round?", ["User 1", "User 2"], key="winner_selection")
        if winner:
            game_data['scores'][winner] += 1
            game_data['current_round'] += 1
            update_game_data(game_data, sha)
            st.success(f"{winner} wins Round {game_data['current_round'] - 1}!")
    

if __name__ == "__main__":
    app()
