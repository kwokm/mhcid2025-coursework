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
pins = [13, 29, 33, 40]  # Replace with your actual GPIO pin numbers

# Pin functions:
# pins[0] (13): Play wav-path1 of current character
# pins[1] (29): Play wav-path2 of current character
# pins[2] (33): Previous character
# pins[3] (40): Next character

# Character data from JSON
characters = []
current_character_index = 0

# Map keyboard keys to pins for testing
key_to_pin_map = {
    'w': pins[0],  # Play wav-path1
    'e': pins[1],  # Play wav-path2
    's': pins[2],  # Previous character
    'd': pins[3]   # Next character
}


def setup():
    # Setup GPIO pins if available
    if RPI_AVAILABLE:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        for pin in pins:
            print ("setting up pin", pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def load_characters_from_json():
    """
    Load character data from currentResponse.json
    """
    global characters, current_character_index
    
    try:
        with open('currentResponse.json', 'r') as file:
            data = json.load(file)
            print(data)
            
        if 'response' in data and isinstance(data['response'], list) and data['response']:
            characters = data['response']
            current_character_index = 0
            print(f"Loaded {len(characters)} characters. Current character: {characters[current_character_index]['name']}")
        else:
            print('Invalid JSON format: response array is missing or empty', file=sys.stderr)
            
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
        toysToStoriesDisplay.display_character(character['name'], character['title'], current_character_index)

    print(f"Switched to: {character['name']} - {character['title']}")

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
        toysToStoriesDisplay.display_character_name(character['name'], character['title'], current_character_index)
    print(f"Switched to: {character['name']} - {character['title']}")

def play_audio(file_path):
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
    
    print(f'Playing audio: {file_path}')
    
    try:
        # Determine the platform and use appropriate audio player
        if sys.platform == 'darwin':  # macOS
            current_process = subprocess.Popen(['afplay', file_path])
            current_process.wait()
        elif sys.platform.startswith('linux'):  # Linux (including Raspberry Pi)
            current_process = subprocess.Popen(['paplay', file_path])
            current_process.wait()
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
        
    if pin == pins[0]:  # Play wav-path1
        if 'wav-path1' in character:
            audio_path = './audiofiles' + character['wav-path1']
            threading.Thread(target=play_audio, args=(audio_path,)).start()
        else:
            print(f"No wav-path1 for character {character['name']}")
            
    elif pin == pins[1]:  # Play wav-path2
        if 'wav-path2' in character:
            audio_path = './audiofiles' + character['wav-path2']
            threading.Thread(target=play_audio, args=(audio_path,)).start()
        else:
            print(f"No wav-path2 for character {character['name']}")
            
    elif pin == pins[2]:  # Previous character
        switch_to_previous_character()
        
    elif pin == pins[3]:  # Next character
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
    print('Keyboard testing enabled:')
    print('  W: Play first sound of current character')
    print('  A: Play second sound of current character')
    print('  S: Switch to previous character')
    print('  D: Switch to next character')
    
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
            if not RPI_AVAILABLE:
                key = get_char()
                # Exit on Ctrl+C
                if key == '\x03':
                    print('Exiting...')
                    break
                    
                # Handle w, a, s, d keys
                if key in ['w', 'e', 's', 'd']:
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