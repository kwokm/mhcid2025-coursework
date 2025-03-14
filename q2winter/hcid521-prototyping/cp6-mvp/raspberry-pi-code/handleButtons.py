import json
import os
import subprocess
import threading
import time
import tty
import sys
import termios
import logging
sys.path.append('./displaycode/mycode')
import toysToStoriesDisplay


# Define global variables for audio playback
play_lock = threading.Lock()
is_playing = False
current_process = None  # Variable to track the current audio process

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
    global characters, current_character_index
    
    try:
        print("DEBUG - Attempting to load currentResponse.json")
        with open('currentResponse.json', 'r') as file:
            data = json.load(file)
            print("DEBUG - Successfully loaded JSON data")
            
        # Check if the JSON has the expected structure
        if 'toys' not in data:
            print("Warning: currentResponse.json does not contain 'toys' field")
            return

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
        
        print(f"Current character: {characters[current_character_index]['name']} the {characters[current_character_index]['title']}")
        return characters
            
    except FileNotFoundError:
        print('currentResponse.json not found.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error loading characters: {str(e)}', file=sys.stderr)

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
    global current_character_index
    
    if not characters:
        print("No characters loaded")
        return
        
    current_character_index = (current_character_index + 1) % len(characters)
    character = get_current_character()
    if RPI_AVAILABLE:
        toysToStoriesDisplay.display_character(character['name'], character['title'], character['key'])

    print(f"Switched to: {character['name']} - {character['title']}")
    print(f"character['key'] = {character['key']}")

def switch_to_previous_character():
    """
    Switch to the previous character in the list
    """
    global current_character_index
    
    if not characters:
        print("No characters loaded")
        return
        
    current_character_index = (current_character_index - 1) % len(characters)
    character = get_current_character()
    if RPI_AVAILABLE:
        toysToStoriesDisplay.display_character(character['name'], character['title'], character['key'])
    print(f"Switched to: {character['name']} - {character['title']}")
    print(f"character['key'] = {character['key']}")

def play_audio(file_path, pin_index):
    """
    Play audio file using the appropriate command for the platform
    """
    global is_playing, current_process
    
    # Cancel any currently playing audio
    with play_lock:
        if is_playing and current_process:
            print("Canceling current playback")
            try:
                current_process.terminate()
                current_process.wait(timeout=1)  # Wait for process to terminate
            except (subprocess.TimeoutExpired, ProcessLookupError):
                # If process doesn't terminate gracefully, force kill it
                try:
                    current_process.kill()
                except:
                    pass
            current_process = None
        
        is_playing = True
    
    character = get_current_character()
    word_info = None
    
    # Handle different vocab structures
    if 'vocab' in character:
        if isinstance(character['vocab'], list):
            # Direct list of vocab items
            if pin_index < len(character['vocab']):
                word_info = character['vocab'][pin_index]
        elif isinstance(character['vocab'], dict) and 'vocab' in character['vocab']:
            # Nested vocab structure
            if pin_index < len(character['vocab']['vocab']):
                word_info = character['vocab']['vocab'][pin_index]
    
    if word_info and 'word' in word_info:
        print(f'Playing audio: {file_path} for word {word_info["word"]}')
    else:
        print(f'Playing audio: {file_path}')
    
    # Debug: Print absolute path and check if file exists
    abs_path = os.path.abspath(file_path)
    print(f"DEBUG - Absolute path: {abs_path}")
    print(f"DEBUG - File exists: {os.path.exists(abs_path)}")
    
    try:
        # Determine the platform and use appropriate audio player
        if sys.platform == 'darwin':  # macOS
            current_process = subprocess.Popen(['afplay', file_path])
            current_process.wait()
        elif sys.platform.startswith('linux'):  # Linux (including Raspberry Pi)
            # Debug: List directory contents
            dir_path = os.path.dirname(abs_path)
            print(f"DEBUG - Directory contents of {dir_path}:")
            try:
                files = os.listdir(dir_path)
                for f in files:
                    print(f"  - {f}")
            except Exception as e:
                print(f"DEBUG - Error listing directory: {str(e)}")
                
            # Try different audio players in order
            players = [
                ['paplay', file_path],
                '''
                ['aplay', file_path],
                ['mplayer', file_path],
                ['mpg123', file_path],
                ['omxplayer', file_path]
                '''
            ]
            success = False
            for player_cmd in players:
                try:
                    print(f"DEBUG - Trying to play with {player_cmd[0]}")
                    current_process = subprocess.Popen(player_cmd)
                    current_process.wait()
                    success = True
                    break
                except (subprocess.SubprocessError, FileNotFoundError) as e:
                    print(f"DEBUG - Failed to play with {player_cmd[0]}: {str(e)}")
                    continue
            
            if not success:
                print("ERROR - All audio players failed")
        else:  # Windows or other
            print(f'Unsupported platform: {sys.platform}', file=sys.stderr)
    except subprocess.SubprocessError as e:
        print(f'Error playing audio: {str(e)}', file=sys.stderr)
    except FileNotFoundError:
        print(f'Audio file not found: {file_path}', file=sys.stderr)
    finally:
        with play_lock:
            is_playing = False
            current_process = None

def handle_key_press(key):
    """
    Handle key press events
    """
    if key in key_to_pin_map:
        pin = key_to_pin_map[key]
        print(f"Key '{key}' pressed, simulating button press on pin {pin}")
        handle_pin_action(pin)

def handle_pin_action(pin):
    """
    Handle actions based on which pin was activated
    """
    character = get_current_character()
    
    if not character:
        print("No character selected")
        return
    
    # Debug: Print current working directory
    print(f"DEBUG - Current working directory: {os.getcwd()}")
    
    # Handle audio buttons
    if pin in [pins[0], pins[1], pins[2], pins[3]]:
        # Find which button index was pressed
        button_index = pins.index(pin)
        
        # Get vocab data based on character structure
        audio_path = None
        audio_file = None
        
        if 'vocab' in character:
            if isinstance(character['vocab'], list):
                # Direct list structure
                if button_index < len(character['vocab']):
                    vocab_item = character['vocab'][button_index]
                    if 'audio' in vocab_item:
                        # Use os.path.join to avoid double slashes
                        audio_file = vocab_item['audio'].lstrip('/')  # Remove leading slash if present
            elif isinstance(character['vocab'], dict) and 'vocab' in character['vocab']:
                # Nested vocab structure
                if button_index < len(character['vocab']['vocab']):
                    vocab_item = character['vocab']['vocab'][button_index]
                    if 'audio' in vocab_item:
                        # Use os.path.join to avoid double slashes
                        audio_file = vocab_item['audio'].lstrip('/')  # Remove leading slash if present
        
        if audio_file:
            # Try different path combinations
            possible_paths = [
                os.path.join(path, audio_file),                      # ./audiofiles/path/to/file.wav
                os.path.join(os.getcwd(), path, audio_file),         # /full/path/to/audiofiles/path/to/file.wav
                os.path.join(os.getcwd(), 'audiofiles', audio_file), # /full/path/to/audiofiles/path/to/file.wav (explicit)
                os.path.join('audiofiles', audio_file),              # audiofiles/path/to/file.wav
                audio_file                                           # path/to/file.wav (as is)
            ]
            
            # Find the first path that exists
            for p in possible_paths:
                if os.path.exists(p):
                    audio_path = p
                    print(f"DEBUG - Found audio file at: {audio_path}")
                    break
                else:
                    print(f"DEBUG - Audio file not found at: {p}")
            
            # If no path exists, try to find the file in the audiofiles directory
            if not audio_path and os.path.exists('audiofiles'):
                print("DEBUG - Searching in audiofiles directory...")
                for root, dirs, files in os.walk('audiofiles'):
                    for file in files:
                        if file == os.path.basename(audio_file):
                            audio_path = os.path.join(root, file)
                            print(f"DEBUG - Found audio file at: {audio_path}")
                            break
                    if audio_path:
                        break
            
            if audio_path:
                threading.Thread(target=play_audio, args=(audio_path, button_index)).start()
            else:
                print(f"No audio file found for {audio_file}")
                # Try using aplay instead of paplay as a fallback
                if sys.platform.startswith('linux'):
                    fallback_path = os.path.join('audiofiles', audio_file)
                    print(f"DEBUG - Trying fallback with aplay: {fallback_path}")
                    threading.Thread(target=lambda: subprocess.call(['aplay', fallback_path]), args=()).start()
        else:
            print(f"No audio found for button {button_index+1} on character {character['name']}")
            
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

def start_listening():
    """
    Start listening for keyboard input and GPIO events
    """
    
    print('Button monitoring started. Press Ctrl+C to exit.')
    print('Keyboard testing enabled: QWER for audio, DF to switch characters.')
    
    # Display current character
    character = get_current_character()
    if character:
        print(f"Current character: {character['name']} - {character['title']}")
    
    # Setup GPIO event detection
    if RPI_AVAILABLE:
        setup_gpio_events()
    
    try:
        # Main loop for keyboard input
        while True:
                key = get_char()
                # Exit on Ctrl+C
                if key == '\x03':
                    print('Exiting...')
                    break
                    
                # Handle w, a, s, d keys
                if key in ['q','w','e','r','d','f']:
                    handle_key_press(key)
                    
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
    finally:
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

