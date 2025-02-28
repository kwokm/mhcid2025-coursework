const { exec } = require('child_process');
const readline = require('readline');

// Define the GPIO pins to monitor (using BCM numbering)
const pins = [17, 27, 22, 23]; // Replace with your actual GPIO pin numbers

// Define audio files to play for each pin
let audioFiles = {
    17: './audiofiles/cartoon/Cartoon Balloon Rubbing 07.wav',
    27: './audiofiles/cartoon/Cartoon Voice Dippity Doo Goofy 01.wav',
    22: './audiofiles/science-fiction/Science Fiction Sci-Fi Electronic Robot Droid 97.wav',
    23: './audiofiles/animals/Animal Mammal Carnivore Cat Tiger Roar 01.wav'
};

// Function to update audio files from JSON
export function updateAudioFiles(jsonString) {
    try {
        // Parse the JSON string
        const data = JSON.parse(jsonString);
        
        // Check if the response array exists and has items
        if (data.response && Array.isArray(data.response) && data.response.length > 0) {
            // Create a new mapping for the pins and audio files
            const newAudioFiles = {};
            
            // Map each response item to a pin
            data.response.forEach((item, index) => {
                if (index < pins.length && item['wav-path']) {
                    // Add './audiofiles' prefix to the path
                    newAudioFiles[pins[index]] = './audiofiles' + item['wav-path'];
                }
            });
            
            // Update the audioFiles object
            audioFiles = newAudioFiles;
            console.log('Audio files updated successfully:', audioFiles);
        } else {
            console.error('Invalid JSON format: response array is missing or empty');
        }
    } catch (error) {
        console.error('Error updating audio files:', error.message);
    }
}

// Map keyboard keys to pins for testing
const keyToPinMap = {
    'w': 17,
    'a': 27,
    's': 22,
    'd': 23
};

// Track if audio is currently playing to prevent overlapping playback
let isPlaying = false;

// Function to play audio file
function playAudio(file) {
    if (isPlaying) return;
    
    isPlaying = true;
    console.log(`Playing audio: ${file}`);
    
    // Use afplay for macOS audio playback
    exec(`afplay "${file}"`, (error) => {
        isPlaying = false;
        if (error) {
            console.error(`Error playing audio: ${error}`);
        }
    });
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

export function startListening() {
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
}

console.log('Button monitoring started. Press Ctrl+C to exit.');
console.log('Keyboard testing enabled: Press W, A, S, or D to simulate button presses.');