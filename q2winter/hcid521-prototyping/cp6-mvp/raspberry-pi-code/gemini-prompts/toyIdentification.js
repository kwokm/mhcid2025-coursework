const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require('@google/generative-ai');
const { GoogleAIFileManager } = require('@google/generative-ai/server');

const apiKey = 'AIzaSyD1rgVz8vdJRIzpYOtrR6wWQmk3M1OI2iE';
const genAI = new GoogleGenerativeAI(apiKey);
const fileManager = new GoogleAIFileManager(apiKey);

/**
 * Uploads the given file to Gemini.
 *
 * See https://ai.google.dev/gemini-api/docs/prompting_with_media
 */
async function uploadToGemini(path, mimeType) {
  const uploadResult = await fileManager.uploadFile(path, {
    mimeType,
    displayName: path,
  });
  const file = uploadResult.file;
  console.log(`Uploaded file ${file.displayName} as: ${file.name}`);
  return file;
}

const model = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction:
    'You are a toy identification system. For each image you see:\n1. Identify the toy in the image\n2. Provide ONLY the most essential name/character in 1-2 words maximum\n3. Do not include descriptions, explanations, or qualifiers\n4. Focus on the main character/toy identity only\n5. Give the toy a creative name\n\nExamples:\n- For a blue dinosaur plush toy → "Dinosaur" or "Blue Dino" for the Item & "Azul" for the name\n- For a LEGO Darth Vader figure → "Sith" for the Item & "Darth Vader" for the name',
});

const generationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 8192,
  responseMimeType: 'application/json',
  responseSchema: {
    type: 'object',
    properties: {
      Item: {
        type: 'string',
      },
      Name: {
        type: 'string',
      },
    },
    required: ['Item', 'Name'],
  },
};

export async function identifyToy(imagePath, imageType, message) {
  // TODO Make these files available on the local file system
  // You may need to update the file paths
  const files = [await uploadToGemini(imagePath, imageType)];

  const chatSession = model.startChat({
    generationConfig,
    history: [
      {
        role: 'user',
        parts: [
          {
            fileData: {
              mimeType: files[0].mimeType,
              fileUri: files[0].uri,
            },
          },
        ],
      },
    ],
  });

  const result = await chatSession.sendMessage(message);
  return result.response.text();
}

// identifyToy("", "");
