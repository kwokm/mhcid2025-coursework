const rpio = require('rpio');

// Define the GPIO pin number connected to the button
const buttonPin = 40; // GPIO 17 (physical pin 11)

// Configure the GPIO pin as an input with a pull-up resistor
rpio.open(buttonPin, rpio.INPUT, rpio.PULL_UP);

console.log(`Listening for button presses on GPIO pin ${buttonPin}...`);

// Function to handle button press
function handleButtonPress() {
  console.log('Button Pressed!');
  // You can add more actions here if needed
}

// Set up an interval to check the button state periodically
const checkIntervalMs = 20; // Check every 50 milliseconds (adjust as needed)
let lastButtonState = 1; // Assume button is initially not pressed (pulled high)

setInterval(() => {
  const currentButtonState = rpio.read(buttonPin);
  console.log(rpio.read(buttonPin));

  // Button press detection (when button pulls the pin LOW - because of pull-up)
  if (currentButtonState === 0 && lastButtonState === 1) {
    handleButtonPress();
  }

  lastButtonState = currentButtonState;
}, checkIntervalMs);

// Keep the script running indefinitely
process.stdin.resume();

// Optional: Handle program termination (e.g., Ctrl+C)
process.on('SIGINT', () => {
  console.log(' \nExiting gracefully, cleaning up...');
  rpio.close(buttonPin); // Close the GPIO pin
  process.exit(0);
});