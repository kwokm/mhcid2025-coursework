var rpio = require('rpio');
const { exec } = require('child_process');
const readline = require('readline');

// Define the GPIO pins to monitor (using BCM numbering)
const pins = [17, 27, 22, 23]; // Replace with your actual GPIO pin numbers

// Define audio files to play for each pin
const audioFiles = {
    17: '/path/to/audio1.mp3',
    27: '/path/to/audio2.mp3',
    22: '/path/to/audio3.mp3',
    23: '/path/to/audio4.mp3'
};

// Map keyboard keys to pins for testing
const keyToPinMap = {
    'w': 17,
    'a': 27,
    's': 22,
    'd': 23
};

// Initialize all pins as inputs with pull-up resistors
pins.forEach(pin => {
    rpio.open(pin, rpio.INPUT, rpio.PULL_UP);
    console.log(`Initialized pin ${pin} for button input`);
});

// Track if audio is currently playing to prevent overlapping playback
let isPlaying = false;

// Function to play audio file
function playAudio(file) {
    if (isPlaying) return;
    
    isPlaying = true;
    console.log(`Playing audio: ${file}`);
    
    // Use omxplayer for Raspberry Pi audio playback
    exec(`omxplayer "${file}"`, (error) => {
        isPlaying = false;
        if (error) {
            console.error(`Error playing audio: ${error}`);
        }
    });
}

// Callback function for button press
function buttonPressCallback(pin) {
    // Debounce: wait a short time to avoid rapid changes
    rpio.msleep(20);
    
    // If pin is high after debounce, it was a false trigger
    if (rpio.read(pin)) return;
    
    console.log(`Button pressed on pin ${pin}`);
    
    // Play the corresponding audio file
    if (audioFiles[pin]) {
        playAudio(audioFiles[pin]);
    } else {
        console.log(`No audio file defined for pin ${pin}`);
    }
}

// Function to handle key press events
function handleKeyPress(key) {
    const pin = keyToPinMap[key];
    if (pin) {
        console.log(`Key '${key}' pressed, simulating button press on pin ${pin}`);
        if (audioFiles[pin]) {
            playAudio(audioFiles[pin]);
        } else {
            console.log(`No audio file defined for pin ${pin}`);
        }
    }
}

// Set up polling for each pin
pins.forEach(pin => {
    rpio.poll(pin, buttonPressCallback, rpio.POLL_LOW);
});

// Set up keyboard input for testing
readline.emitKeypressEvents(process.stdin);
if (process.stdin.isTTY) {
    process.stdin.setRawMode(true);
}

process.stdin.on('keypress', (str, key) => {
    // Exit on Ctrl+C
    if (key.ctrl && key.name === 'c') {
        console.log('Exiting...');
        process.exit();
    }
    
    // Handle w, a, s, d keys
    if (['w', 'a', 's', 'd'].includes(str)) {
        handleKeyPress(str);
    }
});

console.log('Button monitoring started. Press Ctrl+C to exit.');
console.log('Keyboard testing enabled: Press W, A, S, or D to simulate button presses.');