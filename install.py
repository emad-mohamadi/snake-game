import subprocess
import sys
import os


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))


def install_package():
    try:
        # Ensure pip is up-to-date
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

        # Install the package
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '.'])

        input("Installation complete. You can now run the game using the 'snake' command.\nPress Enter to continue.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        input("Please ensure you have an active internet connection and try again.\nPress Enter to continue.")


if __name__ == "__main__":
    install_package()
