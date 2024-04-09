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
        if index == 0:  # Leader gets a crown
            container.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:bold;">{user}:</span>
                    <span>{score} points <span style="color:gold;">&nbsp;&#x1F451;</span></span>
                </div>
                """, unsafe_allow_html=True)
        else:
            container.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:bold;">{user}:</span>
                    <span>{score} points</span>
                </div>
                """, unsafe_allow_html=True)

def app():

    st.image("https://photo-assets.masters.com/images/pics/misc/Masters_Lockup1A_RGB.png", width=200)

    st.title("Augusta Aces: The 2024 Masters Golf Betting Challenge")
    
    # Fetch the current game data from GitHub
    game_data, sha = read_game_data()
    if not game_data:
        st.stop()

    st.write(f"Current Round: {game_data['current_round']}")

    col1, col2 = st.columns([3, 1])
    
    with col1:
        if game_data['current_round'] > 4:
            winner = max(game_data['scores'], key=game_data['scores'].get)
            st.header(f"Game Over - Winner: {winner}")
            return
        
        st.subheader("Select Your Golfer")
        for user in ["User 1", "User 2"]:

            last_selection = game_data['selections'].get(user, "")

            # Ensure each selection box is uniquely keyed
            selection_key = f"{user}_selection_{game_data['current_round']}"
            selected_golfer = st.selectbox(f"{user}, select your golfer:",
                                                         ["Ludvig Aberg (SWEDEN)", 
                                                          "Byeong Hun An (KOREA)", 
                                                          "Akshay Bhatia (UNITED STATES)",
                                                          "Keegan Bradley (UNITED STATES)",
                                                          "Sam Burns (UNITED STATES)",
                                                          "Patrick Cantlay (UNITED STATES)", 
                                                          "Wyndham Clark (UNITED STATES)",
                                                          "Eric Cole (UNITED STATES)",
                                                          "Corey Conners (CANADA)",
                                                          "Fred Couples (UNITED STATES)",
                                                          "Cameron Davis (AUSTRALIA)",
                                                          "Jason Day (AUSTRALIA",
                                                          "Bryson DeChambeau (UNITED STATES)",
                                                          "Santiago de la Fuente (A) (MEXICO)",
                                                          "Nick Dunlap (UNITED STATES)",
                                                          "Austin Eckroat (UNITED STATES)",
                                                          "Harris English (UNITED STATES)",
                                                          "Tony Finau (UNITED STATES)",
                                                          "Matt Fitzpatrick (ENGLAND)",
                                                          "Tommy Fleetwood (ENGLAND)",
                                                          "Rickie Fowler (UNITED STATES)",
                                                          "Ryan Fox (NEW ZEALAND)",
                                                          "Sergio Garcia (SPAIN)",
                                                          "Lucas Glover (UNITED STATES)",
                                                          "Emiliano Grillo (ARGENTINA)",
                                                          "Adam Hadwin (CANADA)",
                                                          "Brian Harman (UNITED STATES)",
                                                          "Tyrrell Hatton (ENGLAND)",
                                                          "Stewart Hagestad (A) (UNITED STATES)",
                                                          "Russell Henley (UNITED STATES)", 
                                                          "Ryo Hisatsune (JAPAN)",
                                                          "Lee Hodges (UNITED STATES)",
                                                          "Nicolai Hojgaard (DENMARK)",
                                                          "Max Homa (UNITED STATES)",
                                                          "Viktor Hovland (NORWAY)",
                                                          "Sungjae Im (KOREA)",
                                                          "Stephan Jaeger (GERMANY)",
                                                          "Dustin Johnson (UNITED STATES)",
                                                          "Zach Johnson (UNITED STATES)",
                                                          "Si Woo Kim (KOREA)",
                                                          "Tom Kim (KOREA)",
                                                          "Chris Kirk (UNITED STATES)",
                                                          "Kurt Kitayama (UNITED STATES)",
                                                          "Jake Knapp (UNITED STATES)",
                                                          "Brooks Koepka (UNITED STATES)",
                                                          "Christo Lamprecht (A) (SOUTH AFRICA)",
                                                          "Min Woo Lee (AUSTRALIA)",
                                                          "Luke List (UNITED STATES)",
                                                          "Shane Lowry (IRELAND)",
                                                          "Peter Malnati (UNITED STATES)",
                                                          "Hideki Matsuyama (JAPAN)",
                                                          "Denny McCarthy (UNITED STATES)",
                                                          "Rory Mcllroy (NORTHERN IRELAND)",
                                                          "Adrian Meronk (POLAND)",
                                                          "Phil Mickelson (UNITED STATES)",
                                                          "Grayson Murray (UNITED STATES)",
                                                          "Taylor Moore (UNITED STATES)",
                                                          "Joaquín Niemann (CHILE)",
                                                          "Collin Morikawa (UNITED STATES)",
                                                          "José María Olazábal (SPAIN)", 
                                                          "Thorbjorn Olesen (DENMARK)",
                                                          "Matthieu Pavon (FRANCE)",
                                                          "J.T. Poston (UNITED STATES)",
                                                          "Jon Rahm (SPAIN)",
                                                          "Patrick Reed (UNITED STATES)",
                                                          "Justin Rose (ENGLAND)",
                                                          "Xander Schauffele (UNITED STATES)",
                                                          "Scottie Scheffler (UNITED STATES)",
                                                          "Adam Schenk (UNITED STATES)",
                                                          "Charl Schwartzel (SOUTH AFRICA)",
                                                          "Adam Scott (AUSTRALIA)",
                                                          "Neal Shipley (A) (UNITED STATES)",
                                                          "Vijay Singh (FIJI)",
                                                          "Cameron Smith (AUSTRALIA)",
                                                          "Jordan Spieth (UNITED STATES)",
                                                          "Sepp Straka (AUSTRIA)",
                                                          "Jasper Stubbs (A) (AUSTRALIA)",
                                                          "Nick Taylor (CANADA)",
                                                          "Sahith Theegala (UNITED STATES)",
                                                          "Justin Thomas (UNITED STATES)",
                                                          "Erik van Rooyen (SOUTH AFRICA)",
                                                          "Camilo Villegas (COLOMBIA)",
                                                          "Bubba Watson (UNITED STATES)",
                                                          "Mike Weir (CANADA)",
                                                          "Danny Willett (ENGLAND)",
                                                          "Gary Woodland (UNITED STATES)",
                                                          "Tiger Woods (UNITED STATES)",
                                                          "Cameron Young (UNITED STATES)",
                                                          "Will Zalatoris (UNITED STATES)"], index=golfers.index(last_selection), key=selection_key)
                        
            game_data['selections'][user] = selected_golfer

            # Display the locked-in player for this user
            st.write(f"Locked in Player: {game_data['selections'][user]}")

        
        if st.button("Lock in Selections"):
            update_game_data(game_data, sha)
            # Use session_state to track that selections are locked in for this round
            st.session_state['selections_locked'] = True

        if 'selections_locked' in st.session_state and st.session_state['selections_locked']:
            # Display confirmation message
            st.markdown("Your selections have been locked in for this round.")

        st.image("https://github.com/johannesaschoff/johannesaschoff/blob/main/2016-MASTERS-COURSE-MAP.jpg?raw=true", width=200, use_column_width='always')

    
    with col2:
        display_leaderboard(game_data['scores'], col2)


if __name__ == "__main__":
    app()
