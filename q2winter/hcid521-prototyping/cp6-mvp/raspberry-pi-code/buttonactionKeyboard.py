import json
import os
import subprocess
import threading
import time
import tty
import sys
import termios
import logging

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use BCM pin numbering to match your pin definitions
    RPI_AVAILABLE = True
    play_lock = threading.Lock()
    is_playing = False
except ImportError:
    print("RPi.GPIO module not available. Running in keyboard-only mode.")
    RPI_AVAILABLE = False

# Define the GPIO pins to monitor (using BOARD numbering)
pins = [13, 29, 33, 40]  # Replace with your actual GPIO pin numbers

# Define audio files to play for each pin
audio_files = {
    pins[0]: './audiofiles/cartoon/Cartoon Balloon Rubbing 07.wav',
    pins[1]: './audiofiles/cartoon/Cartoon Voice Dippity Doo Goofy 01.wav',
    pins[2]: './audiofiles/science-fiction/Science Fiction Sci-Fi Electronic Robot Droid 97.wav',
    pins[3]: './audiofiles/animals/Animal Mammal Carnivore Cat Tiger Roar 01.wav'
}

# Map keyboard keys to pins for testing
key_to_pin_map = {
    'w': pins[0],
    'a': pins[1],
    's': pins[2],
    'd': pins[3]
}


def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # Setup GPIO pins if available
    if RPI_AVAILABLE:
        for pin in pins:
            print ("setting up pin", pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def update_audio_files(json_string):
    """
    Update audio files from JSON string and save to currentResponse.json
    """
    try:
        # Parse the JSON string
        data = json.loads(json_string)
        
        # Check if the response array exists and has items
        if 'response' in data and isinstance(data['response'], list) and data['response']:
            # Create a new mapping for the pins and audio files
            new_audio_files = {}
            
            # Map each response item to a pin
            for index, item in enumerate(data['response']):
                if index < len(pins) and 'wav-path' in item:
                    # Add './audiofiles' prefix to the path
                    new_audio_files[pins[index]] = './audiofiles' + item['wav-path']
            
            # Update the audio_files dictionary
            global audio_files
            audio_files = new_audio_files
            print(f'Audio files updated successfully: {audio_files}')
        else:
            print('Invalid JSON format: response array is missing or empty', file=sys.stderr)
        
        # Write the json_string to currentResponse.json
        with open('./currentResponse.json', 'w') as file:
            file.write(json_string)
            print('currentResponse.json updated successfully.')
            
    except json.JSONDecodeError as e:
        print(f'Error updating audio files: {str(e)}', file=sys.stderr)
    except IOError as e:
        print(f'Error writing to currentResponse.json: {str(e)}', file=sys.stderr)

def initialize_audio_files():
    """
    Initialize audio files from currentResponse.json
    """
    try:
        with open('currentResponse.json', 'r') as file:
            data = file.read()
            update_audio_files(data)
    except FileNotFoundError:
        print('currentResponse.json not found. Using default audio files.', file=sys.stderr)
    except json.JSONDecodeError as e:
        print(f'Error parsing currentResponse.json: {str(e)}', file=sys.stderr)
    except Exception as e:
        print(f'Error initializing audio files: {str(e)}', file=sys.stderr)

def play_audio(file_path):
    """
    Play audio file using the appropriate command for the platform
    """
    global is_playing
    
    with play_lock:
        if is_playing:
            return
        
        is_playing = True
    
    print(f'Playing audio: {file_path}')
    
    try:
        # Determine the platform and use appropriate audio player
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['afplay', file_path], check=True)
        elif sys.platform.startswith('linux'):  # Linux (including Raspberry Pi)
            subprocess.run(['paplay', file_path], check=True)
        else:  # Windows or other
            print(f'Unsupported platform: {sys.platform}', file=sys.stderr)
    except subprocess.SubprocessError as e:
        print(f'Error playing audio: {str(e)}', file=sys.stderr)
    except FileNotFoundError:
        print(f'Audio file not found: {file_path}', file=sys.stderr)
    finally:
        with play_lock:
            is_playing = False

def handle_key_press(key):
    """
    Handle key press events
    """
    if key in key_to_pin_map:
        pin = key_to_pin_map[key]
        print(f"Key '{key}' pressed, simulating button press on pin {pin}")
        
        if pin in audio_files:
            # Start audio playback in a separate thread to avoid blocking
            threading.Thread(target=play_audio, args=(audio_files[pin],)).start()
        else:
            print(f'No audio file defined for pin {pin}')

def handle_gpio_event(channel):
    """
    Handle GPIO events (button press)
    """
    # Debounce
    time.sleep(0.02)
    
    # Check if the button is still pressed after debounce
    if GPIO.input(channel) == GPIO.HIGH:
        print(f"Button pressed on pin {channel}")
        if channel in audio_files:
            threading.Thread(target=play_audio, args=(audio_files[channel],)).start()
        else:
            print(f'No audio file defined for pin {channel}')

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
    print('Keyboard testing enabled: Press W, A, S, or D to simulate button presses.')
    
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
            if key in ['w', 'a', 's', 'd']:
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
    # Initialize audio files from currentResponse.json on startup
    initialize_audio_files()
    
    # Start listening for keyboard input and GPIO events
    start_listening() 