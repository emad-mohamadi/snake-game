import subprocess
import sys
from os import path


def uninstall_package():
    try:
        # Uninstall the package
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'uninstall', 'snake'])

        input("Uninstallation complete. The Snake-Game has been removed.\nPress Enter to continue.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        input("Please try running the script again or uninstall the package manually using pip.\nPress Enter to continue.")


if __name__ == "__main__":
    uninstall_package()
