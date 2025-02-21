

let stars = [];
let speed = 10; // Initial zoom speed
let xpos = 0;
let starDensity = 800;
let minSpeed = 5; // Minimum zoom speed limit

// Variables to store accelerometer data from CPX
let accelX = 0;
let accelY = 0;

// --- Color Palette for Stars ---
let starColors = [
  [255, 255, 255],       // White
  [255, 240, 255],       // Slightly Warm White (Ivory/Cream)
  [230, 245, 255],       // Very Cool White (Light Steel Blue)
  [180, 220, 255],       // Light Blue (Sky Blue)
];
// --- End Colors

let serial; // Serial port object

function setup() {
  createCanvas(1280, 800);
  for (let i = 0; i < starDensity; i++) {
    stars.push(new Star());
  }

}



function draw() {
  background(0);

  // --- Control Speed based on accelY (Forward/Backward Tilt) ---
  speed += accelY * 1; // Adjust multiplier to control speed sensitivity
  speed = constrain(speed, minSpeed, 80); // Limit speed range
  xpos += accelX * 1; // Adjust multiplier to control speed sensitivity
  xpos = constrain(xpos, -1.5, 1.5); // Limit xpos range


  push(); // Start a new drawing state

  // --- Control Horizontal Zoom Direction based on accelX (Left/Right Tilt) ---
  translate(width / 2 + xpos * 200, height / 2); // Adjust multiplier for horizontal shift amount

  for (let i = 0; i < stars.length; i++) {
    stars[i].update();
    stars[i].show();
  }

  pop(); // Restore original drawing state

 
  /* // --- UNCOMMENT FOR DEBUGGING SERIAL DATA and SPEED ---  
  fill(255);
  textSize(16);
  textAlign(LEFT, TOP);
  text(`Speed: ${speed.toFixed(2)}, XPos: ${xpos.toFixed(2)}, AccelY: ${accelY.toFixed(2)}`, 10, 10); */
}

class Star {
  constructor() {
    this.x = random(-width, width);
    this.y = random(-height, height);
    this.z = random(0, width);
    this.pz = this.z;
    this.size = map(this.z, 0, width, 0, 4);
    this.color = random(starColors);
  }

  update() {
    this.z -= speed; // Use the updated 'speed' variable

    if (this.z < 1) {
      this.z = width;
      this.pz = this.z;
      this.x = random(-width, width);
      this.y = random(-height, height);
    }
  }

  show() {
    fill(this.color);
    noStroke();

    let sx = map(this.x / this.z, 0, 1, 0, width);
    let sy = map(this.y / this.z, 0, 1, 0, height);

    let r = map(this.z, 0, width, this.size * 2, this.size);

    ellipse(sx, sy, r, r);

    let px = map(this.x / this.pz, 0, 1, 0, width);
    let py = map(this.y / this.pz, 0, 1, 0, height);

    stroke(this.color);
    strokeWeight(r);
    this.pz = this.z;
    line(px, py, sx, sy);
    noStroke();
  }
}

function keyPressed() {
    if (key === 's' || key === 'S') {
      accelY = -0.5; // Simulate backward tilt (decrease speed)
    } else if (key === 'w' || key === 'W') {
      accelY = 0.5; // Simulate forward tilt (increase speed)
    } else if (key === 'a' || key === 'A') {
      accelX = .04; // Simulate left tilt (shift zoom right)
    } else if (key === 'd' || key === 'D') {
      accelX = -.04; // Simulate right tilt (shift zoom left)dd
    }
    if (key === 'r'){
        accelY = 0;
    }
    if (key === 'f'){
        accelX = 0;
    }
  }
