# Tabletop Wargame Assistant

## Requirements

- Python 3.11.6
- A camera on video input 2 (can be changed in Camera.py)
- A defined set of operatives in encodingsInUse.py
- Installed libraries: `pip install -r requirements.txt`
- A calibrated camera matrix

NOTE: The screen size is not scalable - it is designed to run on a monitor that is 2560x1440

## How to play

- Setup your camera pointing down at the gameboard
- Run src/interface/InterfacePyGame.py

- On startup you will be met with a static image of the gameboard
- This is to calibrate the board position
- Click the top left, top right, bottom left and bottom right corners of your gameboard in that order
- The main game should then appear
- Clicking on an operative will allow you to select it and display the line of sight
- You can then remove or update an operatives state using the buttons in the bottom left


- You can create your own markers using the generateCircle.py

# I really need to clean up this repo
