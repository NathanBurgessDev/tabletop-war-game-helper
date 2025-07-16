# Tabletop Wargame Assistant

## Report

The full Dissertation report can be found [here](https://github.com/NathanBurgessDev/tabletop-war-game-helper/blob/486b84c6d3fb91c0c6fbb1c145b8ab680fe0b240/Dissertation/20363169_dissertation.pdf)

Information regarding requirements gathering, software management, testing, user analysis and troubleshooting can be found within the report.


## Requirements

- Python 3.11.6
- A camera on video input 2 (can be changed in Camera.py)
- A defined set of operatives in encodingsInUse.py
- Installed libraries: `pip install -r requirements.txt`
- A calibrated camera matrix

NOTE: The screen size is not scalable - it is designed to run on a monitor that is 2560x1440

## How to play
1. Setup your camera pointing down at the gameboard
2. Run src/interface/InterfacePyGame.py

3. On startup you will be met with a static image of the gameboard
4. This is to calibrate the board position
5. Click the top left, top right, bottom left and bottom right corners of your gameboard in that order
6. The main game should then appear
7. Clicking on an operative will allow you to select it and display the line of sight
8. You can then remove or update an operatives state using the buttons in the bottom left

More comprehensive instructions - including physical setup - can be found within the full report.

## Notes

If you are embarking on a similar project please do feel free to contact me and use this work to assist you.
