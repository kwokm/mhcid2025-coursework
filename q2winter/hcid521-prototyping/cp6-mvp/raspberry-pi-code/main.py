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

def setup():
    chars = []
    
    try:
        with open('currentResponse.json', 'r') as file:
            data = json.load(file)
            print(data)
            
        if 'response' in data and isinstance(data['response'], list) and data['response']:
            chars = data['response']
        else:
            print('Invalid JSON format: response array is missing or empty', file=sys.stderr)
            
    except FileNotFoundError:
        print('currentResponse.json not found.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error loading characters: {str(e)}', file=sys.stderr)

    import assetSetup
    assetSetup.download_images(chars)
    assetSetup.convert_images_to_bmps(chars)

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
    setup()
    setupScreen()
    setupAudio()

main()