import sys
import json
import os
import subprocess
import time
import RPi.GPIO as GPIO

sys.path.append('./gemini-prompts')
sys.path.append('./displaycode/mycode')
import buttonactionKeyboard
# import wordsToAudio

def setupScreen():
    import toysToStoriesDisplay
    toysToStoriesDisplay.display_loading()
    data = json.load(open('currentResponse.json'))
    print(data)
    toysToStoriesDisplay.display_toys_to_stories(data["response"][0]["word"], data["response"][1]["word"], data["response"][2]["word"], data["response"][3]["word"])
    toysToStoriesDisplay.shutdown_display()

def setupAudio():
    buttonactionKeyboard.initialize_audio_files();
    buttonactionKeyboard.setup();
    buttonactionKeyboard.start_listening();

def main():
    setupScreen()
    setupAudio()

main()