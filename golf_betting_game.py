import streamlit as st
import json
import os

# File path for the JSON file to store data
data_file = 'golf_betting_game_data.json'

# Initialize or load game data
def load_game_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    else:
        return {'current_round': 1, 'scores': {'User 1': 0, 'User 2': 0}, 'selections': {}}

# Save game data
def save_game_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)

# App main function
def app():
    # Load the game state
    game_data = load_game_data()
    
    golfers = ['Golfer 1', 'Golfer 2', 'Golfer 3', 'Golfer 4', 'Golfer 5']
    
    st.title("Golf Betting Game")
    
    if game_data['current_round'] > 4:
        st.header("Game Over")
        winner = max(game_data['scores'], key=game_data['scores'].get)
        st.subheader(f"{winner} Wins!")
        st.write(game_data['scores'])
        return
    
    st.header(f"Round {game_data['current_round']}")
    for user in ['User 1', 'User 2']:
        game_data['selections'][user] = st.selectbox(f"{user}, select your golfer for round {game_data['current_round']}:", golfers, key=user)
    
    if st.button('Lock in Selections'):
        save_game_data(game_data)
        st.write("Selections locked in. Refresh the page to see the current selections.")
        
    winner = st.radio("Select the round winner:", ['None', 'User 1', 'User 2'])
    if winner != 'None':
        game_data['scores'][winner] += 1
        game_data['current_round'] += 1
        save_game_data(game_data)
        st.success(f"{winner} wins Round {game_data['current_round'] - 1}!")
        st.button('Next Round')

if __name__ == "__main__":
    app()
