input.buttonA.onEvent(ButtonEvent.Click, function () {
  count++;
  if (count == 0) {
    // First click - start gradient
    strip.show();
    setGradientColor(339.79, 55.88, 66.67, 168, 66.16, 77.65);
    control.runInParallel(() => {
      createMovingGradient();
    });
  } else if (count == 1) {
    // setyellow
    setGradientColor(339.79, 55.88, 66.67, 168, 66.16, 77.65);
    strip.setAll(light.rgb(244, 196, 48));
  } else if (count == 2) {
    // yellow to green
    colorTransition(light.rgb(244, 196, 48), light.rgb(108, 185, 91));
  } else if (count == 3) {
    // green to blue to dim
    colorTransition(light.rgb(108, 185, 91), light.rgb(41, 69, 126));
    dim(150, 80, 3000);
  } else if (count == 4) {
    // green to orange
    strip.setBrightness(150);
    control.runInParallel(() => {
      strip.showAnimation(light.rainbowAnimation, 30000);
    });
  } else if (count == 5) {
    dim(150, 10, 10000);
  }
});

function setGradientColor(h1: number, s1: number, v1: number, h2: number, s2: number, v2: number) {
  let hDiff = (h1 - h2) / STRIPSIZE;
  let sDiff = (s1 - s2) / STRIPSIZE;
  let vDiff = (v1 - v2) / STRIPSIZE;
  for (let i = 0; i <= STRIPSIZE - 1; i++) {
    strip.setPixelColor(i, light.hsv(h1 + i * hDiff, s1 + i * sDiff, v1 + i * vDiff));
    strip.show();
  }
}

function createMovingGradient() {
  let cycleTime = 200;
  let currColors = [];

  while (count == 0) {
    for (let i = 0; i <= STRIPSIZE - 1; i++) {
      currColors[i] = strip.pixelColor(i);
    }

    for (let i = 0; i <= STRIPSIZE - 1; i++) {
      if (i === 0) {
        strip.setPixelColor(i, currColors[STRIPSIZE - 1]);
      } else {
        strip.setPixelColor(i, currColors[i - 1]);
      }
      strip.show();
    }
    basic.pause(cycleTime / STRIPSIZE);
  }
}

function colorTransition(color1: number, color2: number) {
  const duration = 3000; // 3 seconds
  const startTime = control.millis();

  // Convert colors to RGB components
  const r1 = (color1 >> 16) & 0xff;
  const g1 = (color1 >> 8) & 0xff;
  const b1 = color1 & 0xff;

  const r2 = (color2 >> 16) & 0xff;
  const g2 = (color2 >> 8) & 0xff;
  const b2 = color2 & 0xff;

  while (true) {
    const elapsed = control.millis() - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Interpolate color components
    const r = r1 + (r2 - r1) * progress;
    const g = g1 + (g2 - g1) * progress;
    const b = b1 + (b2 - b1) * progress;

    // Update all pixels with rounded values
    strip.setAll(light.rgb(Math.round(r), Math.round(g), Math.round(b)));

    if (progress >= 1) break;
    basic.pause(10); // 10ms delay for smooth transition
  }

  // Ensure final color is exact
  strip.setAll(color2);
}

function dim(start: number, end: number, duration: number) {
  const startBrightness = start;
  const endBrightness = end;
  const startTime = control.millis();

  while (true) {
    const elapsed = control.millis() - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // Calculate current brightness
    const currentBrightness = startBrightness - (startBrightness - endBrightness) * progress;

    // Set brightness and update strip
    strip.setBrightness(Math.round(currentBrightness));
    strip.show();

    // Exit loop when duration is reached
    if (progress >= 1) break;

    // Small pause to keep things smooth
    basic.pause(50);
  }

  // Ensure final brightness is exact
  strip.setBrightness(end);
  strip.show();
}

let STRIPSIZE = 14;
let strip = light.createStrip(pins.A1, STRIPSIZE, NeoPixelMode.RGB);
let gradientActive = false;
strip.setBrightness(150);
let count = -1;
