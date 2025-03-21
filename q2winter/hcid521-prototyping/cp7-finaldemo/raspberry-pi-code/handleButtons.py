import json
import os
import subprocess
import threading
import time
import tty
import sys
import termios
import logging
import select
sys.path.append('./displaycode/mycode')
import toysToStoriesDisplay


# Define global variables for audio playback
current_process = None  # Variable to track the current audio process

# Define audio modes and track current mode for each button
AUDIO_MODES = ["original", "pronunciation", "translation"]
button_modes = {0: 0, 1: 0, 2: 0, 3: 0}  # Maps button index to current mode index

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use BCM pin numbering to match your pin definitions
    RPI_AVAILABLE = True
except ImportError:
    print("RPi.GPIO module not available. Running in keyboard-only mode.")
    RPI_AVAILABLE = False

# Define the GPIO pins to monitor (using BOARD numbering)
pins = [40, 36, 32, 3, 16, 29]  # Replace with your actual GPIO pin numbers
pinInitialize = sorted(pins, reverse=True)  # Sort pins from largest to smallest
path = './audiofiles'

# Pin functions:
# pins[0] (40): alternate word1 sound & pronunciation
# pins[1] (36): alternate word2 sound & pronunciation
# pins[2] (32): alternate word3 sound & pronunciation
# pins[3] (7): alternate word4 sound & pronunciation
# pins[4] (16): previous character
# pins[5] (12): next character

# Character data from JSON
characters = []
current_character_index = 0

# Map keyboard keys to pins for testing
key_to_pin_map = {
    'q': pins[0],  # Play first word
    'w': pins[1],  # Play 2nd word
    'e': pins[2],  # play 3rd word
    'r': pins[3],   # Play 4th word
    'd': pins[4],   # back character
    'f': pins[5],   # forward character
}

# Flag to control the main listening loop
should_exit = False

# Cache for audio file existence checks
audio_file_cache = {}

def setup():
    # Setup GPIO pins if available
    if RPI_AVAILABLE:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        for pin in pinInitialize:
            print ("setting up pin", pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def load_characters_from_json():
    """
    Load character data from currentResponse.json
    """
    global characters, current_character_index, lang
    
    try:
        # Check if we already have characters loaded
        if characters:
            print("DEBUG - Characters already loaded, skipping JSON load")
            return characters
            
        print("DEBUG - Attempting to load currentResponse.json")
        
        # Use a cached file if it exists
        json_path = 'currentResponse.json'
        if not os.path.exists(json_path):
            print(f"ERROR - {json_path} not found")
            return None
            
        # Load the JSON file once
        with open(json_path, 'r') as file:
            data = json.load(file)
            print("DEBUG - Successfully loaded JSON data")
            
        # Check if the JSON has the expected structure
        if 'toys' not in data:
            print("Warning: currentResponse.json does not contain 'toys' field")
            return None

        global lang
        lang = data['language']

        characters = data['toys']
        current_character_index = 0
        
        # Debug: Print character information
        print(f"DEBUG - Loaded {len(characters)} characters")
        for i, char in enumerate(characters):
            print(f"DEBUG - Character {i+1}: {char['name']} ({char['title']})")
            
            # Debug vocab structure
            if 'vocab' in char:
                if isinstance(char['vocab'], list):
                    print(f"  - Vocab structure: direct list with {len(char['vocab'])} items")
                    for j, v in enumerate(char['vocab']):
                        print(f"    - Word {j+1}: {v.get('word', 'N/A')} ({v.get('audio', 'No audio')})")
                elif isinstance(char['vocab'], dict) and 'vocab' in char['vocab']:
                    print(f"  - Vocab structure: nested dict with {len(char['vocab']['vocab'])} items")
                    for j, v in enumerate(char['vocab']['vocab']):
                        print(f"    - Word {j+1}: {v.get('word', 'N/A')} ({v.get('audio', 'No audio')})")
                else:
                    print(f"  - Vocab structure: unknown format")
            else:
                print(f"  - No vocab data found")
        
        if characters:
            print(f"Current character: {characters[current_character_index]['name']} the {characters[current_character_index]['title']}")
        
        # Pre-cache audio file existence
        preload_audio_file_cache()
        
        return characters
            
    except FileNotFoundError:
        print('currentResponse.json not found.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error loading characters: {str(e)}', file=sys.stderr)
    
    return None

def preload_audio_file_cache():
    """
    Preload the existence of audio files into a cache to avoid repeated file system checks
    """
    global audio_file_cache
    
    # Clear the cache
    audio_file_cache = {}
    
    # Check audio directories
    audio_dirs = [
        './audiofiles',
        './pronounce-audio',
        './pronounce-translate-audio'
    ]
    
    # Populate cache with file existence information
    for audio_dir in audio_dirs:
        if os.path.exists(audio_dir):
            for filename in os.listdir(audio_dir):
                full_path = os.path.join(audio_dir, filename)
                if os.path.isfile(full_path):
                    audio_file_cache[full_path] = True
    
    print(f"Preloaded {len(audio_file_cache)} audio files into cache")

def file_exists(file_path):
    """
    Check if a file exists, using the cache if available
    """
    if file_path in audio_file_cache:
        return audio_file_cache[file_path]
    
    # If not in cache, check the file system and update cache
    exists = os.path.isfile(file_path)
    audio_file_cache[file_path] = exists
    return exists

def get_current_character():
    """
    Get the current character data
    """
    if characters and 0 <= current_character_index < len(characters):
        return characters[current_character_index]
    return None

def switch_to_next_character():
    """
    Switch to the next character in the list
    """
    global current_character_index, button_modes
    
    if not characters:
        print("No characters loaded")
        return
        
    current_character_index = (current_character_index + 1) % len(characters)
    character = get_current_character()
    if RPI_AVAILABLE:
        toysToStoriesDisplay.display_character(character['name'], character['title'], character['key'])

    # Reset all button modes to 0 (original audio mode)
    for button_index in button_modes:
        button_modes[button_index] = 0
    
    print(f"Switched to: {character['name']} - {character['title']}")
    print(f"character['key'] = {character['key']}")
    print("All button modes reset to original audio mode")

def switch_to_previous_character():
    """
    Switch to the previous character in the list
    """
    global current_character_index, button_modes
    
    if not characters:
        print("No characters loaded")
        return
        
    current_character_index = (current_character_index - 1) % len(characters)
    character = get_current_character()
    if RPI_AVAILABLE:
        toysToStoriesDisplay.display_character(character['name'], character['title'], character['key'])
    
    # Reset all button modes to 0 (original audio mode)
    for button_index in button_modes:
        button_modes[button_index] = 0
        
    print(f"Switched to: {character['name']} - {character['title']}")
    print(f"character['key'] = {character['key']}")
    print("All button modes reset to original audio mode")

def play_audio(file_path, pin_index):
    """
    Play audio file using the appropriate command for the platform
    """
    global current_process
    
    # Always terminate the current process if it exists
    if current_process:
        try:
            current_process.terminate()
        except:
            pass
        current_process = None
    
    # Always kill any audio playback processes based on platform
    if sys.platform == 'darwin':  # macOS
        try:
            # Kill any afplay processes
            subprocess.run(['pkill', '-f', 'afplay'], stderr=subprocess.DEVNULL)
        except Exception:
            pass
    elif sys.platform.startswith('linux'):  # Linux (including Raspberry Pi)
        try:
            # Kill any paplay and aplay processes
            subprocess.run(['pkill', '-f', 'paplay'], stderr=subprocess.DEVNULL)
        except Exception:
            pass
    
    character = get_current_character()
    word_info = None
    
    # Get word info for display purposes
    if 'vocab' in character:
        if isinstance(character['vocab'], list):
            if pin_index < len(character['vocab']):
                word_info = character['vocab'][pin_index]
        elif isinstance(character['vocab'], dict) and 'vocab' in character['vocab']:
            if pin_index < len(character['vocab']['vocab']):
                word_info = character['vocab']['vocab'][pin_index]
    
    if word_info and 'word' in word_info:
        print(f'Playing audio: {file_path} for word {word_info["word"]}')
    else:
        print(f'Playing audio: {file_path}')
    
    # Check if file exists using the cache
    if not file_exists(file_path):
        print(f"ERROR - Audio file not found: {file_path}")
        return
    
    try:
        # Determine the platform and use appropriate audio player
        if sys.platform == 'darwin':  # macOS
            current_process = subprocess.Popen(['afplay', file_path])
            current_process.wait()
        elif sys.platform.startswith('linux'):  # Linux (including Raspberry Pi)
            # Try paplay first (PulseAudio)
            try:
                current_process = subprocess.Popen(['paplay', file_path])
                current_process.wait()
            except (subprocess.SubprocessError, FileNotFoundError):
                # Fallback to aplay if paplay fails
                try:
                    current_process = subprocess.Popen(['aplay', file_path])
                    current_process.wait()
                except (subprocess.SubprocessError, FileNotFoundError) as e:
                    print(f"ERROR - Failed to play audio: {str(e)}")
        else:  # Windows or other
            print(f'Unsupported platform: {sys.platform}', file=sys.stderr)
    except Exception as e:
        print(f'Error playing audio: {str(e)}', file=sys.stderr)
    finally:
        current_process = None

def handle_key_press(key):
    """
    Handle key press events
    """
    if key in key_to_pin_map:
        pin = key_to_pin_map[key]
        print(f"Key '{key}' pressed, simulating button press on pin {pin}")
        handle_pin_action(pin)
    elif key == 'x':  # Use 'x' key to simulate pressing both navigation buttons
        print("'x' key pressed, simulating both navigation buttons pressed")
        restart_main_process()

def handle_pin_action(pin):
    """
    Handle actions based on which pin was activated
    """
    global button_modes
    character = get_current_character()
    
    if not character:
        print("No character selected")
        return
    
    # Handle audio buttons
    if pin in [pins[0], pins[1], pins[2], pins[3]]:
        # Find which button index was pressed
        button_index = pins.index(pin)
        
        # Get the vocab item for this button
        vocab_item = None
        if 'vocab' in character:
            if isinstance(character['vocab'], list):
                if button_index < len(character['vocab']):
                    vocab_item = character['vocab'][button_index]
            elif isinstance(character['vocab'], dict) and 'vocab' in character['vocab']:
                if button_index < len(character['vocab']['vocab']):
                    vocab_item = character['vocab']['vocab'][button_index]
        
        if not vocab_item:
            print(f"No vocabulary item found for button {button_index}")
            return
            
        # Get the current mode for this button
        current_mode = button_modes[button_index]
        
        # Determine which audio file to play based on the current mode
        audio_file = None
        if current_mode == 0:  # Original audio
            if 'audio' in vocab_item:
                audio_file = os.path.join('./audiofiles', f"{vocab_item['audio']}")
        elif current_mode == 1:  # Pronunciation
            if 'word' in vocab_item:
                audio_file = os.path.join('./pronounce-audio', f"{vocab_item['word']}.mp3")
        elif current_mode == 2:  # Translation
            if 'translation' in vocab_item:
                audio_file = os.path.join('./pronounce-translate-audio', f"{vocab_item['translation']}-{lang}.mp3")
        
        # Rotate to the next mode for this button
        button_modes[button_index] = (current_mode + 1) % len(AUDIO_MODES)
        
        # Print the current mode and next mode
        print(f"Button {button_index} - Current mode: {AUDIO_MODES[current_mode]}, Next mode: {AUDIO_MODES[button_modes[button_index]]}")
        
        # Play the audio if a file was found
        if audio_file:
            print(f"Playing {AUDIO_MODES[current_mode]} audio for word: {vocab_item.get('word', 'unknown')}")
            threading.Thread(target=play_audio, args=(audio_file, button_index)).start()
        else:
            print(f"No audio file found for {AUDIO_MODES[current_mode]} mode")
            
    # Handle navigation buttons
    elif pin == pins[4]:  # Previous character
        switch_to_previous_character()
        
    elif pin == pins[5]:  # Next character
        switch_to_next_character()

def handle_gpio_event(channel):
    """
    Handle GPIO events (button press)
    """
    # Debounce
    time.sleep(0.02)
    
    # Check if the button is still pressed after debounce
    if GPIO.input(channel) == GPIO.HIGH:
        print(f"Button pressed on pin {channel}")
        handle_pin_action(channel)

def get_char():
    """
    Get a single character from standard input
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def setup_gpio_events():
    """
    Setup GPIO event detection for all pins
    """
    if not RPI_AVAILABLE:
        return
        
    # Add event detection for each pin (RISING edge = button press)
    for pin in pins:
        GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_gpio_event, bouncetime=20)
    
    print("GPIO event detection set up for pins:", pins)

def check_both_nav_buttons_pressed():
    """
    Check if both navigation buttons (pins 16 and 29) are pressed simultaneously
    Returns True if both buttons are pressed, False otherwise
    """
    if not RPI_AVAILABLE:
        return False
    
    # Get the state of both navigation buttons
    # Note: GPIO.LOW means the button is pressed (active low)
    prev_button_pressed = GPIO.input(pins[4]) == GPIO.LOW
    next_button_pressed = GPIO.input(pins[5]) == GPIO.LOW
    
    # Add a small debounce to avoid false positives
    if prev_button_pressed and next_button_pressed:
        # Wait a small amount of time and check again to confirm
        time.sleep(0.05)
        prev_button_pressed = GPIO.input(pins[4]) == GPIO.LOW
        next_button_pressed = GPIO.input(pins[5]) == GPIO.LOW
    
    return prev_button_pressed and next_button_pressed

def restart_main_process():
    """
    Restart the main process by executing main.py
    """
    global should_exit
    
    print("Both navigation buttons pressed simultaneously! Restarting main process...")
    should_exit = True
    
    # Clean up GPIO before restarting
    if RPI_AVAILABLE:
        GPIO.cleanup()
    
    # Execute main.py in a new process
    try:
        # Use the same Python interpreter that's currently running
        python_executable = sys.executable
        main_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
        
        # Start the new process
        subprocess.Popen([python_executable, main_script])
        
        # Exit the current process
        print("Restarting main process...")
        sys.exit(0)
    except Exception as e:
        print(f"Error restarting main process: {str(e)}", file=sys.stderr)
        should_exit = False

def start_listening():
    """
    Start listening for keyboard input and GPIO events
    """
    global should_exit
    should_exit = False
    
    print('Button monitoring started. Press Ctrl+C to exit.')
    print('Keyboard testing enabled: QWER for audio, DF to switch characters, X to restart.')
    print('Each button press rotates through modes: Original -> Pronunciation -> Translation -> Original')
    print('Press both navigation buttons (pins 16 and 29) simultaneously to restart the main process.')
    
    # Display current character
    character = get_current_character()
    if character:
        print(f"Current character: {character['name']} - {character['title']}")
    
    # Setup GPIO event detection
    if RPI_AVAILABLE:
        setup_gpio_events()
    
    # Create a separate thread for checking button presses if on Raspberry Pi
    if RPI_AVAILABLE:
        def check_buttons_thread():
            while not should_exit:
                if check_both_nav_buttons_pressed():
                    restart_main_process()
                    break
                time.sleep(0.1)
        
        # Start the button checking thread
        button_thread = threading.Thread(target=check_buttons_thread)
        button_thread.daemon = True  # Make thread exit when main thread exits
        button_thread.start()
    
    try:
        # Main loop for keyboard input
        while not should_exit:
            try:
                # Try non-blocking keyboard input with select
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    key = get_char()
                    # Exit on Ctrl+C
                    if key == '\x03':
                        print('Exiting...')
                        break
                    
                    # Handle keys
                    if key in ['q','w','e','r','d','f','x']:
                        handle_key_press(key)
                
                # Small delay to prevent high CPU usage
                time.sleep(0.05)
            except (select.error, ValueError, TypeError) as e:
                # Fallback to blocking input if select doesn't work
                print(f"Warning: Non-blocking input failed ({str(e)}), falling back to blocking input")
                key = get_char()
                # Exit on Ctrl+C
                if key == '\x03':
                    print('Exiting...')
                    break
                
                # Handle keys
                if key in ['q','w','e','r','d','f','x']:
                    handle_key_press(key)
                    
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
    finally:
        # Set exit flag for any threads
        should_exit = True
        # Clean up GPIO on exit
        if RPI_AVAILABLE:
            GPIO.cleanup()

if __name__ == "__main__":
    # Setup GPIO pins
    if RPI_AVAILABLE:
        setup()
    
    # Load characters from JSON
    load_characters_from_json()
    
    # Start listening for keyboard input and GPIO events
    start_listening()

