import sys
from logic import Game
from display import welcome

def get_integer_input(prompt, min_val=1, max_val=30):
    while True:
        try:
            value = input(prompt)
            if value.lower() in ['q', 'quit', 'exit']:
                sys.exit()
            
            value = int(value)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_boolean_input(prompt):
    while True:
        response = input(prompt + " (y/n): ").lower()
        if response in ['q', 'quit', 'exit']:
            sys.exit()
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def main_menu():
    print("\n=== SNAKE GAME CONFIGURATION ===")
    print("Configure your game settings (press 'q' to quit at any time)\n")

    # Game Size
    size = get_integer_input("Enter board size (3-30): ", min_val=3, max_val=30)

    # Wall Mode
    wall_mode = get_boolean_input("Enable wall mode?")

    # Step Time (controls game speed)
    step_time = get_float_input("Enter step time (0.01-0.5, lower = faster): ", 
                                min_val=0.01, max_val=0.5)

    # Autopilot
    autopilot = get_boolean_input("Enable autopilot mode?")

    # Show Path
    show_path = get_boolean_input("Show pathfinding path?")

    # Start game with selected configurations
    welcome()
    snake = Game(
        size=size, 
        wall=wall_mode, 
        step_time=step_time
    )
    snake.run(
        autopilot=autopilot, 
        show_path=show_path
    )

def get_float_input(prompt, min_val=0.01, max_val=0.5):
    while True:
        try:
            value = input(prompt)
            if value.lower() in ['q', 'quit', 'exit']:
                sys.exit()
            
            value = float(value)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main_menu()