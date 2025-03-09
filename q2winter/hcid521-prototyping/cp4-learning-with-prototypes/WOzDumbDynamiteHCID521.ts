function createMovingGradient() {
  let count = 0;
  cycleTime = 8000;
  while (count == 0) {
    let currColors: number[] = [];
    for (let k = 0; k <= STRIPSIZE - 1; k++) {
      currColors[k] = strip.pixelColor(k);
    }
    for (let l = 0; l <= STRIPSIZE - 1; l++) {
      if (l == 0) {
        strip.setPixelColor(l, currColors[STRIPSIZE - 1]);
      } else {
        strip.setPixelColor(l, currColors[l - 1]);
      }
      strip.show();
    }
    basic.pause(cycleTime / STRIPSIZE);
  }
}
function colorTransition(color1: number, color2: number) {
  const duration = 3000;
  startTime2 = control.millis();
  // Convert colors to RGB components
  const r12 = (color1 >> 16) & 0xff;
  const g12 = (color1 >> 8) & 0xff;
  const b12 = color1 & 0xff;
  const r22 = (color2 >> 16) & 0xff;
  const g22 = (color2 >> 8) & 0xff;
  const b22 = color2 & 0xff;
  while (true) {
    elapsed = control.millis() - startTime2;
    progress = Math.min(elapsed / duration, 1);
    // Interpolate color components Update all pixels with
    // rounded values
    strip.setAll(
      light.rgb(
        Math.round(r12 + (r22 - r12) * progress),
        Math.round(g12 + (g22 - g12) * progress),
        Math.round(b12 + (b22 - b12) * progress)
      )
    );
    if (progress >= 1) {
      break;
    }
    basic.pause(5);
  }
  // Ensure final color is exact
  strip.setAll(color2);
}
function transitionPixel(pixel: number, newColor: number) {
  const duration = 3000;
  startTime = control.millis();
  const r1 = (strip.pixelColor(pixel) >> 16) & 0xff;
  const g1 = (strip.pixelColor(pixel) >> 8) & 0xff;
  const b1 = strip.pixelColor(pixel) & 0xff;
  const r2 = (newColor >> 16) & 0xff;
  const g2 = (newColor >> 8) & 0xff;
  const b2 = newColor & 0xff;
  while (true) {
    elapsed = control.millis() - startTime;
    progress = Math.min(elapsed / duration, 1);
    // Update pixel with rounded values
    strip.setPixelColor(
      pixel,
      light.rgb(
        Math.round(r1 + (r2 - r1) * progress),
        Math.round(g1 + (g2 - g1) * progress),
        Math.round(b1 + (b2 - b1) * progress)
      )
    );
    if (progress >= 1) {
      break;
    }
    basic.pause(5);
  }
  // Ensure final color is exact
  strip.setPixelColor(pixel, newColor);
}
function transitionStrip(newColor: number) {
  control.runInParallel(function () {
    transitionPixel(0, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(1, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(2, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(3, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(4, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(5, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(6, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(7, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(8, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(9, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(10, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(11, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(12, newColor);
  });
  control.runInParallel(function () {
    transitionPixel(13, newColor);
  });
}
function adjustBrightness(start: number, end: number, duration: number) {
  startBrightness = start;
  endBrightness = end;
  startTime22 = control.millis();
  while (true) {
    elapsed2 = control.millis() - startTime22;
    progress2 = Math.min(elapsed2 / duration, 1);
    // Calculate current brightness
    currentBrightness = startBrightness - (startBrightness - endBrightness) * progress2;
    // Set brightness and update strip
    strip.setBrightness(Math.round(currentBrightness));
    strip.show();
    // Exit loop when duration is reached
    if (progress2 >= 1) {
      break;
    }
    // Small pause to keep things smooth
    basic.pause(3);
  }
  // Ensure final brightness is exact
  strip.setBrightness(end);
  strip.show();
}
function breathe(start: number, end: number, cycles: number, duration: number) {
  for (let i = 0; i < cycles; i++) {
    adjustBrightness(start, end, duration);
    adjustBrightness(end, start, duration);
  }
}
function setGradientColor(h1: number, s1: number, v1: number, h2: number, s2: number, v2: number) {
  hDiff = (h1 - h2) / (STRIPSIZE - 1);
  sDiff = (s1 - s2) / (STRIPSIZE - 1);
  vDiff = (v1 - v2) / (STRIPSIZE - 1);
  control.runInParallel(function () {
    transitionPixel(0, light.hsv(h1, s1, v1));
  });
  control.runInParallel(function () {
    transitionPixel(1, light.hsv(h2 - 12 * hDiff, s2 - 12 * sDiff, v2 - 12 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(2, light.hsv(h2 - 11 * hDiff, s2 - 11 * sDiff, v2 - 11 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(3, light.hsv(h2 - 10 * hDiff, s2 - 10 * sDiff, v2 - 10 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(4, light.hsv(h2 - 9 * hDiff, s2 - 9 * sDiff, v2 - 9 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(5, light.hsv(h2 - 8 * hDiff, s2 - 8 * sDiff, v2 - 8 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(6, light.hsv(h2 - 7 * hDiff, s2 - 7 * sDiff, v2 - 7 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(7, light.hsv(h2 - 6 * hDiff, s2 - 6 * sDiff, v2 - 6 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(8, light.hsv(h2 - 5 * hDiff, s2 - 5 * sDiff, v2 - 5 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(9, light.hsv(h2 - 4 * hDiff, s2 - 4 * sDiff, v2 - 4 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(10, light.hsv(h2 - 3 * hDiff, s2 - 3 * sDiff, v2 - 3 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(11, light.hsv(h2 - 2 * hDiff, s2 - 2 * sDiff, v2 - 2 * vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(12, light.hsv(h2 - hDiff, s2 - sDiff, v2 - vDiff));
  });
  control.runInParallel(function () {
    transitionPixel(13, light.hsv(h2, s2, v2));
  });
}

function setGradientColorRGB(
  r1: number,
  g1: number,
  b1: number,
  r2: number,
  g2: number,
  b2: number
) {
  const rDiff = (r1 - r2) / (STRIPSIZE - 1);
  const bDiff = (b1 - b2) / (STRIPSIZE - 1);
  const gDiff = (g1 - g2) / (STRIPSIZE - 1);
  control.runInParallel(function () {
    transitionPixel(0, light.rgb(r1, g1, b1));
  });
  control.runInParallel(function () {
    transitionPixel(1, light.rgb(r2 - 12 * rDiff, g2 - 12 * gDiff, b2 - 12 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(2, light.rgb(r2 - 11 * rDiff, g2 - 11 * gDiff, b2 - 11 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(3, light.rgb(r2 - 10 * rDiff, g2 - 10 * gDiff, b2 - 10 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(4, light.rgb(r2 - 9 * rDiff, g2 - 9 * gDiff, b2 - 9 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(5, light.rgb(r2 - 8 * rDiff, g2 - 8 * gDiff, b2 - 8 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(6, light.rgb(r2 - 7 * rDiff, g2 - 7 * gDiff, b2 - 7 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(7, light.rgb(r2 - 6 * rDiff, g2 - 6 * gDiff, b2 - 6 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(8, light.rgb(r2 - 5 * rDiff, g2 - 5 * gDiff, b2 - 5 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(9, light.rgb(r2 - 4 * rDiff, g2 - 4 * gDiff, b2 - 4 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(10, light.rgb(r2 - 3 * rDiff, g2 - 3 * gDiff, b2 - 3 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(11, light.rgb(r2 - 2 * rDiff, g2 - 2 * gDiff, b2 - 2 * bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(12, light.rgb(r2 - rDiff, g2 - gDiff, b2 - bDiff));
  });
  control.runInParallel(function () {
    transitionPixel(13, light.rgb(r2, g2, b2));
  });
}

let vDiff = 0;
let sDiff = 0;
let hDiff = 0;
let currentBrightness = 0;
let progress2 = 0;
let elapsed2 = 0;
let startTime22 = 0;
let endBrightness = 0;
let startBrightness = 0;
let startTime = 0;
let progress = 0;
let elapsed = 0;
let startTime2 = 0;
let cycleTime = 0;
let STRIPSIZE = 0;
let gradientActive = false;
STRIPSIZE = 14;
let strip = light.createStrip(pins.A1, STRIPSIZE, NeoPixelMode.RGB);
strip.setBrightness(15);
transitionStrip(light.rgb(240, 100, 20));
strip.show();
// basic.pause(10000) // wait 10s then start story - 0s
basic.pause(8500); // Green Room - 8s
control.runInParallel(function () {
  transitionPixel(0, light.rgb(58, 106, 30));
});
control.runInParallel(function () {
  transitionPixel(1, light.rgb(58, 106, 30));
});
control.runInParallel(function () {
  transitionPixel(2, light.rgb(58, 106, 30));
});
control.runInParallel(function () {
  transitionPixel(3, light.rgb(58, 106, 30));
});

basic.pause(6000); // Red Balloon 14s
control.runInParallel(function () {
  transitionPixel(13, light.rgb(102, 0, 3));
});
control.runInParallel(function () {
  transitionPixel(12, light.rgb(102, 0, 3));
});
control.runInParallel(function () {
  transitionPixel(11, light.rgb(102, 0, 3));
});

basic.pause(7000); // Cow 21s
control.runInParallel(function () {
  breathe(15, 30, 1, 1200);
});

basic.pause(4000); // bears 25s
control.runInParallel(function () {
  transitionPixel(13, light.rgb(139, 69, 19));
});
control.runInParallel(function () {
  transitionPixel(12, light.rgb(139, 69, 19));
});
control.runInParallel(function () {
  transitionPixel(11, light.rgb(139, 69, 19));
});
basic.pause(1000); // bear roar 26s
control.runInParallel(function () {
  breathe(15, 50, 1, 1100);
});

basic.pause(7000); // Kittens 32s
control.runInParallel(function () {
  breathe(15, 23, 2, 320);
  basic.pause(500);
  breathe(15, 23, 1, 320);
});

basic.pause(10000); // Mouse 42s
control.runInParallel(function () {
  breathe(15, 23, 6, 200);
});

basic.pause(19000); // Lady Hush 62
control.runInParallel(function () {
  breathe(15, 38, 1, 2000);
});

basic.pause(12800); // Cow 75
control.runInParallel(function () {
  breathe(15, 25, 1, 1200);
});

basic.pause(6000); // Goodnight Balloon 80
transitionStrip(light.rgb(240, 100, 20)); // 83
basic.pause(3000);
control.runInParallel(function () {
  breathe(15, 50, 1, 1100);
}); // bears

// 91 kittens
basic.pause(8200);
control.runInParallel(function () {
  breathe(15, 23, 2, 320);
  basic.pause(500);
  breathe(15, 23, 1, 320);
});

// 101 clocks
basic.pause(9000);
control.runInParallel(function () {
  strip.setBrightness(17);
  strip.show();
  basic.pause(600);
  strip.setBrightness(15);
  strip.show();
  basic.pause(600);
  strip.setBrightness(17);
  strip.show();
  basic.pause(600);
  strip.setBrightness(15);
  strip.show();
  basic.pause(600);
  strip.setBrightness(17);
  strip.show();
  basic.pause(600);
  strip.setBrightness(15);
  strip.show();
  basic.pause(600);
  strip.setBrightness(17);
  strip.show();
  basic.pause(60);
  strip.setBrightness(15);
  strip.show();
});

// 114 mouse
basic.pause(13000);
control.runInParallel(function () {
  breathe(15, 19, 6, 200);
});

// 140 transition
basic.pause(21000); // end of audio
// Fade to Atmosphere
setGradientColorRGB(240, 100, 20, 180, 100, 20);
adjustBrightness(15, 5, 3000);
control.runInParallel(function () {
  createMovingGradient();
});
