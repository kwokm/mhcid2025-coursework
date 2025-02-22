let y = 0
let x = 0
let threshold = 400

// NEEDED SO THAT MACOS DOES NOT IGNORE DEVICE AS "SPAM"
basic.pause(3000)

// MUST IMPORT KEYBOARD EXTENSION IN ONLINE MAKECODE IDE

forever(function () {
    x = input.acceleration(Dimension.X)
    y = input.acceleration(Dimension.Y)
    // Adjust this threshold value as needed: Check for
    // forward tilt (tilted downward → negative Y)
    if (y < 0 - threshold) {
        keyboard.type("w")
    } else if (y > threshold) {
        keyboard.type("s")
    } else {
        keyboard.type("r")
    }
    // Check for left tilt (tilted left → negative X)
    if (x < 0 - threshold) {
        keyboard.type("a")
    } else if (x > threshold) {
        keyboard.type("d")
    } else {
        keyboard.type("f")
    }
    // Short pause so the loop doesn’t run too fast:
    basic.pause(50)
})
