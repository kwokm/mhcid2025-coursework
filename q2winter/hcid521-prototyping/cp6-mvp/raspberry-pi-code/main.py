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

chars = [];

def setupChars():
    
    try:
        with open('currentResponse.json', 'r') as file:
            data = json.load(file)

        # Check if the JSON has the expected structure
        if 'toys' not in data:
            print("Warning: currentResponse.json does not contain 'toys' field")
            return

        chars = data['toys']
            
    except FileNotFoundError:
        print('currentResponse.json not found.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error loading characters: {str(e)}', file=sys.stderr)

    import assetSetup
    '''
    assetSetup.download_json()
    '''
    assetSetup.download_images(chars)
    assetSetup.download_pronunciation_audio(chars)
    assetSetup.convert_images_to_bmps(chars)

def setupScreen():
    if RPI_AVAILABLE:
        import toysToStoriesDisplay
        toysToStoriesDisplay.display_loading()
        data = json.load(open('currentResponse.json'))
        toys = data['toys']
        toysToStoriesDisplay.clear_display()
        toysToStoriesDisplay.display_character(toys[0]['name'], toys[0]['title'], toys[0]['key'], True)

def setupAudio():
    handleButtons.load_characters_from_json();
    handleButtons.setup();
    handleButtons.start_listening();

def main():
    if RPI_AVAILABLE:
        import toysToStoriesDisplay
        toysToStoriesDisplay.display_loading()
    setupChars()
    setupScreen()
    setupAudio()
    if RPI_AVAILABLE:
        data = json.load(open('currentResponse.json'))
        toys = data['toys']
        toysToStoriesDisplay.clear_display()
        toysToStoriesDisplay.display_character(toys[0]['name'], toys[0]['title'], toys[0]['key'], True)

main()