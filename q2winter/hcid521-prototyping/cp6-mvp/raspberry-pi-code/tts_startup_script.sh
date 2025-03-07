#!/bin/bash

# Startup script to activate virtual environment and run Python script

# FOLLOW THESE INSTRUCTIONS TO INSTALL!
# Make the script executable: chmod +x tts_startup_script.sh
# Add the script to your crontab:
# crontab -e
# @reboot /home/pi/tts_startup_script.sh

# Run the Python script
/usr/bin/tmux new-session -d -s startup_process "cd /home/pi/ && source venv-toys-to-stories/bin/activate && /usr/bin/python3 /home/pi/index.py"

# Keep the script running (optional - remove if not needed)
# This prevents the terminal from closing immediately after execution
# read -p "Press Enter to exit..."