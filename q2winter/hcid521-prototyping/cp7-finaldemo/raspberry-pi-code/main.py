import sys
import json
import os
import subprocess
import time
import concurrent.futures
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

chars = []

def load_json_data():
    """Load JSON data once and return it to avoid repeated loading"""
    try:
        with open('currentResponse.json', 'r') as file:
            data = json.load(file)

        # Check if the JSON has the expected structure
        if 'toys' not in data:
            print("Warning: currentResponse.json does not contain 'toys' field")
            return None

        return data
            
    except FileNotFoundError:
        print('currentResponse.json not found.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error loading characters: {str(e)}', file=sys.stderr)
    
    return None

def setupChars():
    import assetSetup
    global chars
    global lang
    
    assetSetup.download_json()
    # Load JSON data
    data = load_json_data()
    if not data:
        return
    
    chars = data['toys']
    lang = data['language']
    
    # Create a thread pool for parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks to the executor
        download_images_future = executor.submit(assetSetup.download_images, chars)
        download_audio_future = executor.submit(assetSetup.download_pronunciation_audio, chars, lang)
        
        # Wait for downloads to complete before starting conversion
        download_images_future.result()
        download_audio_future.result()
        
        # Now convert images to BMPs
        assetSetup.convert_images_to_bmps(chars)

def setupScreen():
    if RPI_AVAILABLE:
        import toysToStoriesDisplay
        toysToStoriesDisplay.display_loading()
        
        # Use the global chars variable instead of reloading JSON
        if chars and len(chars) > 0:
            toysToStoriesDisplay.clear_display()
            toysToStoriesDisplay.display_character(chars[0]['name'], chars[0]['title'], chars[0]['key'], True)

def setupAudio():
    handleButtons.load_characters_from_json()
    handleButtons.setup()
    handleButtons.start_listening()

def main():
    start_time = time.time()
    
    if RPI_AVAILABLE:
        import toysToStoriesDisplay
        toysToStoriesDisplay.display_loading()
    
    setupChars()
    setupScreen()
    setupAudio()
    
    end_time = time.time()
    print(f"Setup completed in {end_time - start_time:.2f} seconds")

main()