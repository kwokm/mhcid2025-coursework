#!/bin/bash

# Script to update soundboard thoroughly and then launch
bash /home/pi/update_files.py
sudo apt-get update
bash /home/pi/launch_soundboard.sh

# Keep the script running (optional - remove if not needed)
# This prevents the terminal from closing immediately after execution
# read -p "Press Enter to exit..."