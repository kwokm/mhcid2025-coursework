import sys
import json
import os
import subprocess
import time
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO is not available on this platform")

sys.path.append('./gemini-prompts')
sys.path.append('./displaycode/mycode')
sys.path.append('./buttonactionKeyboard')

import buttonactionKeyboard
# import wordsToAudio

def setupScreen():
    import toysToStoriesDisplay
    toysToStoriesDisplay.display_loading()
    data = json.load(open('currentResponse.json'))
    print(data)
    toysToStoriesDisplay.clear_display()
    toysToStoriesDisplay.display_character_name("Azul", "Little Whale")

def setupAudio():
    buttonactionKeyboard.setup()
    # Load characters from JSON
    buttonactionKeyboard.load_characters_from_json()
    
    # Start listening for keyboard input and GPIO events
    buttonactionKeyboard.start_listening() 

def main():
    setupScreen()
    setupAudio()

main()