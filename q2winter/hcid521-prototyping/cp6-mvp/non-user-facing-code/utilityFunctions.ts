/**
 * Recursively extracts all values with a specific label from a JSON object
 * @param obj - The JSON object to search through
 * @param targetKey - The key/label to search for
 * @returns An array of values associated with the target key
 */
export function extractJsonValues(targetKey: string, obj: any): any[] {
  const results: any[] = [];

  // Helper function to recursively search through the object
  function search(currentObj: any): void {
    // Base case: if currentObj is null or not an object, return
    if (currentObj === null || typeof currentObj !== 'object') {
      return;
    }

    // Check if the current object is an array
    if (Array.isArray(currentObj)) {
      // Recursively search through each item in the array
      for (const item of currentObj) {
        search(item);
      }
    } else {
      // For objects, check each key-value pair
      for (const [key, value] of Object.entries(currentObj)) {
        // If the key matches our target, add the value to results
        if (key === targetKey) {
          results.push(value);
        }

        // Recursively search through nested objects/arrays
        search(value);
      }
    }
  }

  // Start the recursive search
  search(obj);
  return results;
}

/**
 * Concatenates an array of strings with an optional delimiter
 * @param strings - The array of strings to concatenate
 * @param delimiter - Optional separator between strings (defaults to empty string)
 * @returns The concatenated string
 */
export function concatenateStrings(strings: string[], delimiter: string = ''): string {
  if (!strings || !Array.isArray(strings)) {
    return '';
  }

  return strings.join(delimiter);
}

/**
 * Determines the MIME type of a file based on its extension
 * @param filePath - The path to the file
 * @returns The MIME type as a string
 */
export function getMimeType(filePath: string): string {
  if (!filePath) {
    return 'application/octet-stream'; // Default MIME type for unknown files
  }

  const extension = filePath.toLowerCase().split('.').pop() || '';

  const mimeTypes: Record<string, string> = {
    // Images
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    gif: 'image/gif',
    bmp: 'image/bmp',
    webp: 'image/webp',
    svg: 'image/svg+xml',
    tiff: 'image/tiff',
    tif: 'image/tiff',

    // Audio
    mp3: 'audio/mpeg',
    wav: 'audio/wav',
    ogg: 'audio/ogg',
    flac: 'audio/flac',
    m4a: 'audio/mp4',

    // Video
    mp4: 'video/mp4',
    webm: 'video/webm',
    avi: 'video/x-msvideo',
    mov: 'video/quicktime',
    wmv: 'video/x-ms-wmv',

    // Documents
    pdf: 'application/pdf',
    doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    xls: 'application/vnd.ms-excel',
    xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ppt: 'application/vnd.ms-powerpoint',
    pptx: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    txt: 'text/plain',
    rtf: 'application/rtf',

    // Web
    html: 'text/html',
    htm: 'text/html',
    css: 'text/css',
    js: 'text/javascript',
    json: 'application/json',
    xml: 'application/xml',

    // Archives
    zip: 'application/zip',
    rar: 'application/x-rar-compressed',
    tar: 'application/x-tar',
    gz: 'application/gzip',
    '7z': 'application/x-7z-compressed',
  };

  return mimeTypes[extension] || 'application/octet-stream';
}

// Example usage with the provided JSON
const exampleJson = {
  Story: {
    'Life Lesson':
      "It's okay to be different! Your unique qualities are what make you special and wonderful. Embrace who you are, and don't worry about being like everyone else.",
    'Page Contents': [
      'Once upon a time, in a lush green jungle, lived a little tiger named Growly.\nGrowly loved to play with his friend Shelly the Turtle, but Growly had a secret.',
      'Growly couldn\'t roar! All the other tigers had big, loud ROARS, but Growly\'s roar was just a tiny squeak.\n"Squeak!" went Growly. He felt very sad.',
      '"I want to roar like a real tiger!" Growly said to Shelly.\nShelly smiled. "But Growly, your squeak is special!"',
      'Growly didn\'t think so. He tried to roar again. He puffed out his chest and opened his mouth WIDE.\n"Squeak!" went Growly. "Oh, dear," he sighed.',
      'Shelly had an idea. "Let\'s try something different!" she said. "Close your eyes and think of something that makes you happy."\nGrowly closed his eyes. He thought of sunny days and playing with Shelly.',
      'He opened his mouth. "Happy..." he whispered. It wasn\'t a roar, but it was a kind, gentle sound.\nShelly clapped her hands. "See, Growly? You have your own special voice!"',
      "Growly smiled. Maybe Shelly was right. Maybe he didn't need to roar to be a real tiger.\nHe used his gentle voice to tell Shelly a funny story, and they both laughed and played all day long.",
      "From that day on, Growly was happy being himself. He learned that it's okay to be different, and that his quiet voice was special in its own way.",
    ],
    'Recommended Vocabulary Words': {
      'Vocabulary Word': [
        {
          Definition: 'When tigers talk very loud',
          'Translated Word': 'Roar',
          Word: 'Roar',
        },
        {
          Definition: 'Where Growly and Shelly live with big trees',
          'Translated Word': 'Jungle',
          Word: 'Jungle',
        },
        {
          Definition: 'How Growly feels when he plays with Shelly',
          'Translated Word': 'Happy',
          Word: 'Happy',
        },
        {
          Definition: 'Something that makes Growly different',
          'Translated Word': 'Special',
          Word: 'Special',
        },
      ],
    },
    Title: 'Growly Finds His Roar',
    'Two Sentence Summary':
      "Growly the Tiger can't roar, which makes him sad because all tigers should roar. With the help of his friend, Shelly the Turtle, Growly learns that it's okay to be different and that his quiet voice is special too.",
  },
};

// Example of extracting all "Definition" values
/*
const definitions = extractValues("Definition", exampleJson);
console.log("Definitions:", definitions); */
