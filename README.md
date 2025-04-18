# 🐍 Terminal Snake Game

A classic Snake game implemented in Python that runs in your terminal.\
~ By The Marboro Team

## Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Uninstallation](#uninstallation)
- [Project Structure](#project-structure)
- [Marboro Team](#marboro-team)
- [Contact](#contact)

## Features
- Classic snake gameplay
- Simple and intuitive controls
+ AI mode (Autopilot)
+ Multiple different foods
+ Obstacles
+ Local signup & login
+ Saving highscores
+ Local leaderboard
+ Adjusting speed & game size


## Requirements
+ Python 3.6+
+ Packages:
    > `keyboard 0.13.5` [🔗](https://github.com/boppreh/keyboard)\
    > `pygame 2.5+` [🔗](https://github.com/pygame/pygame)

## Installation
0. Ensure that pip & git is installed on your device ([install pip](https://pip.pypa.io/en/stable/installation/), [install git](https://github.com/git-guides/install-git)):
   ```bash
   pip --version
   git --version
   ```
1. Clone the repository:
   ```bash
   git clone https://github.com/emad-mohamadi/snake-game.git
   ```
2. Install the package:
   ```bash
   pip install snake-game
   ```
## Usage
To start the game, simply run `snake` command anywhere in terminal.
> [!WARNING]
> In Linux OS, the `keyboard` module might require root access.
## Uninstallation
To uninstall the game, run:
   ```bash
   pip uninstall snake
   ```
## Project Structure
  ```
   .snake-game/
   ├── snake/
   │   ├── __init__.py
   │   ├── main.py             # Runs the game
   │   ├── logic.py            # Game logic and menus
   │   ├── navigate.py         # AI algorithm
   │   ├── display.py          # Terminal interface
   │   ├── pygamesnake.py      # Pygame interface
   │   ├── logo.txt            # Team ascii logo
   │   ├── pics/               # Pygame pictures
   │   │   ├── apple.png
   │   │   ├── block.png
   │   │   ├── body.png
   │   │   ├── snake-head-down.png
   │   │   ├── snake-head-left.png
   │   │   ├── snake-head-right.png
   │   │   └── snake-head-up.png
   │   ├── data.json           # Game data
   │   └── users.json          # Pygame data
   ├── setup.py                # Game install setup
   ├── requirements.txt        # Dependencies
   └── README.md               # Project README
   ```
## Marboro Team
> [@emad-mohamadi](https://github.com/emad-mohamadi)\
 [@melow-git](https://github.com/melow-git)\
 [@danial-fazel](https://github.com/danial-fazel)\
 [@Mhdig0](https://github.com/Mhdig0)

## Contact
>Mail: semadmhmdi@gmail.com \
Telegram: [@emad_mohammadi](https://t.me/emad_mohammadi)
----
## **Enjoy it** 🍵
