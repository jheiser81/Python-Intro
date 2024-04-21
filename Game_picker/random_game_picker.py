import tkinter as tk
from tkinter import messagebox
import requests
import random
import webbrowser

# Get the Steam API key from a text file
def get_api_key(path):
    """ 
    This function reads the Steam API key from a text file and returns it as a string.
    The with statement automatically closes the file when the block of code is exited. 
    The 'r' argument is used to open the file in read mode. 
    The strip() method is used to remove any leading or trailing whitespace from the string.
    """
    with open(path, 'r') as file: 
        return file.read().strip()

# Get a list of all games owned by the user with the given Steam ID
def get_all_games(key, steam_id):
    """
    This function takes a Steam API key and a Steam ID as input and returns a list of dictionaries containing information about the games owned by the user.
    The url variable is constructed using an f-string to insert the key and steam_id values into the URL.
    The requests.get() function is used to send a GET request to the Steam API and store the response in the response variable. The response is then converted to JSON format using the .json() method.
    The data variable is used to access the 'games' key in the JSON response, which contains a list of dictionaries with information about each game.
    A list comprehension is used to iterate over the games in the data variable and extract the 'name', 'appid', and 'playtime_forever' values for each game. 
    These values are stored in a dictionary and added to the games list. 
    The function then returns the games list.
    """
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={steam_id}&include_appinfo=true&format=json"
    response = requests.get(url)
    data = response.json()['response']['games']
    return [{'name': game['name'], 'appid': game['appid'], 'playtime_forever': game['playtime_forever']} for game in data]

# Get a list of unplayed games owned by the user with the given Steam ID
def get_unplayed_games(key, steam_id):
    """
    This function takes a Steam API key and a Steam ID as input and returns a list of dictionaries containing information about the unplayed games owned by the user.
    The get_all_games() function is called with the key and steam_id arguments to retrieve a list of all games owned by the user.
    A list comprehension is used to iterate over the games in the all_games list and filter out the games with a 'playtime_forever' value of 0.
    The function then returns the filtered list of unplayed games.
    """
    all_games = get_all_games(key, steam_id)
    return [game for game in all_games if game['playtime_forever'] == 0]

# Suggest a random game from the list of unplayed games
def suggest_game(games):
    """
    This function takes a list of games as input and returns a random game from the list.
    The random.choice() function is used to select a random game from the games list and return it.
    """
    game = random.choice(games)
    return game
     
# Get the game type from the user
def get_game_type(window):
    """
    This function creates a drop-down menu using the OptionMenu widget from the tkinter module to allow the user to select the game type.
    The game_type variable is created using the StringVar() function, which is a tkinter variable type that stores the selected value from the drop-down menu. 
    The set() method is used to set the default value of the drop-down menu to "All".
    The window parameter is used to specify the parent window for the drop-down menu.
    The OptionMenu widget is created with the window as the parent window, the game_type variable as the selected value, and the options "All" and "Unplayed" as the drop-down menu options.
    The pack() method is called on the OptionMenu widget to display it in the window.
    The function then returns the game_type variable.
    """ 
    game_type = tk.StringVar()
    game_type.set("All") # default value
    
    game_type_option_menu = tk.OptionMenu(window, game_type, "All", "Unplayed")
    game_type_option_menu.pack()
    
    return game_type

# Function to create the GUI for the game picker application           
def create_gui(key, steam_id):
    """
    This function creates a GUI window using the tkinter module to allow the user to select the game type and receive a random game suggestion.
    The window variable is created using the Tk() function from the tkinter module to create a new window.
    The title() method is called on the window variable to set the title of the window to "Game Picker".
    The on_submit() function is defined to handle the submission of the game type selection and display a random game suggestion to the user.
    The game_type_var variable is created using the StringVar() function to store the selected game type from the radio buttons.
    Two radio buttons are created using the Radiobutton widget from the tkinter module to allow the user to select the game type ("All" or "Unplayed").
    The text parameter is used to set the text displayed next to each radio button.
    The variable parameter is set to the game_type_var variable to store the selected value.
    The value parameter is set to "all" for the "All" radio button and "unplayed" for the "Unplayed" radio button.
    The submit_button variable is created using the Button widget from the tkinter module to create a button that calls the on_submit() function when clicked.
    The text parameter is used to set the text displayed on the button.
    The command parameter is set to the on_submit function to specify the function to call when the button is clicked.
    The pack() method is called on the all_games_radio, unplayed_games_radio, and submit_button widgets to display them in the window.
    The window.mainloop() function is called to start the main event loop and display the window to the user.
    """
    window = tk.Tk()
    window.title("Random Game Picker")
    
    welcome_message = tk.Label(window, text="Welcome to the Random Game Picker!")
    instructions_message = tk.Label(window, text="Select from ALL your games or only UNPLAYED games, then click Submit to get a random game suggestion.")
        
    welcome_message.pack()
    instructions_message.pack()
    
    game_type_var = tk.StringVar(value='unplayed')
    all_games_radio = tk.Radiobutton(window, text='All games', variable=game_type_var, value='all')
    unplayed_games_radio = tk.Radiobutton(window, text='Unplayed games', variable=game_type_var, value='unplayed')
    
    def submit_button_click():
        on_submit(game_type_var.get(), key, steam_id)
    
    submit_button = tk.Button(window, text='Submit', command=submit_button_click, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
    
    all_games_radio.pack()
    unplayed_games_radio.pack()
    submit_button.pack()
    
    window.mainloop()
    
def on_submit(game_type, key, steam_id):
    # Get a list of games based on the selected game type, key, and steam_id
    if game_type == 'all':
        games = get_all_games(key, steam_id)
    else:
        games = get_unplayed_games(key, steam_id)
    
    while True:
        # Suggest a random game from the list of games
        game = suggest_game(games)
        
        # Display a message box with the name of the suggested game
        tk.messagebox.showinfo("Game Suggestion:", f"Try playing: {game['name']}")
        
        # Ask the user if they want to launch the suggested game
        launch = tk.messagebox.askyesno("Launch Game", f"Would you like to launch {game['name']}?")
        
        if launch:
            game_url = f"steam://run/{game['appid']}"
            webbrowser.open(game_url)
            break
        else:
            # Ask the user if they want another random game suggestion
            another_game = tk.messagebox.askyesno("Another Game", "Would you like to suggest another game?")
            
            if not another_game:
                break
                      
# Get the path to the Steam API key file                 
key_path = "C:\\Users\\Administrator\\Desktop\\GitHub Repos\\Game_picker\\Steam_API_Key.txt"
steam_id = 76561198042102876
key = get_api_key(key_path)

# Call the function to create and start the GUI 
create_gui(key, steam_id)