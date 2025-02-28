var rpio = require('rpio');

const buttonPin = 40;

// Using physical pin numbers! This is GPIO 21
rpio.open(buttonPin, rpio.INPUT, rpio.PULL_UP);

function pollcb(pin)
{
        /*
         * Wait for a small period of time to avoid rapid changes which
         * can't all be caught with the 1ms polling frequency.  If the
         * pin is no longer down after the wait then ignore it.
         */
        rpio.msleep(20);

        if (rpio.read(pin))
                return;

        console.log('Button pressed on pin P%d', pin);
}

rpio.poll(buttonPin, pollcb, rpio.POLL_LOW);