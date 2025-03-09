import sys
import json
import os
import subprocess
import time
try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    print("RPi.GPIO module not available. Running in keyboard-only mode.")
    RPI_AVAILABLE = False

sys.path.append('./gemini-prompts')
sys.path.append('./displaycode/mycode')
import handleButtons
# import wordsToAudio

def setupScreen():
    if RPI_AVAILABLE:
        import toysToStoriesDisplay
        toysToStoriesDisplay.display_loading()
        data = json.load(open('currentResponse.json'))
        print(data)
        toysToStoriesDisplay.clear_display()
        toysToStoriesDisplay.display_character("Azul", "Little Whale", 0)

def setupAudio():
    handleButtons.load_characters_from_json()
    handleButtons.setup();
    handleButtons.start_listening();

def main():
    setupScreen()
    setupAudio()

main()