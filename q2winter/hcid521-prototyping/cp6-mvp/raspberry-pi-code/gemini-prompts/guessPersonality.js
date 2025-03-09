const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require('@google/generative-ai');

const apiKey = 'AIzaSyD1rgVz8vdJRIzpYOtrR6wWQmk3M1OI2iE';
const genAI = new GoogleGenerativeAI(apiKey);

// Original model for story translation
const translationModel = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction:
    'This is part of a prompt chain helping bilingual parents connect with their children and teach them new words. You will receive a language and a JSON string in two messages.  Please translate the JSON file to the designated language.\n\n\nSample JSON to be received:\n"{\n  Story: {\n    "Life Lesson": "Sometimes, even when we feel small and insignificant, we have special talents that can help others and make a big difference.",\n    "Page Contents": [ "Page 1: Once upon a time, in a cozy little corner of a toy box, lived a small, round Tapioca. Tapioca wasn\'t just any toy; he was a Sumikko Gurashi character, always a bit shy and often feeling like he didn\'t quite fit in. He watched the other toys play, wishing he could join in but feeling too timid to try.",\n      "Page 2: One sunny morning, the toys decided to play hide-and-seek. \\"I\'ll never be found,\\" Tapioca mumbled. \\"I\'m too small and plain!\\" But then, he noticed something. A little lost button, separated from his teddy bear. The teddy bear looked sad. \\"Oh no, he lost his button!\\"",\n      "Page 3: Tapioca knew he had to help. He waddled towards the teddy bear, rolling along the way. \\"Excuse me,\\" squeaked Tapioca. \\"I see you\'ve lost something!\\" The teddy bear looked down, surprised to see the little Tapioca.",\n      "Page 4: Tapioca, with all his might, pushed the button closer to the teddy bear. The teddy bear carefully picked it up. \\"Oh, thank you, little Tapioca!\\" exclaimed the teddy bear, his face lighting up. \\"You found my missing button!\\"",\n      "Page 5: The teddy bear, now with his button safely back on, gave Tapioca a big hug. \\"You might be small, Tapioca,\\" he said, \\"but you have a very big heart!\\" All the other toys gathered around, cheering for Tapioca. He wasn\'t just a shy little toy anymore; he was a hero!",\n      "Page 6: From that day on, Tapioca realized that even though he felt small, he had the ability to help others and make them happy. He joined in the games, not feeling shy anymore, knowing that his kindness made him special."\n    ],\n    "Recommended Vocabulary Words": {\n      "Vocabulary Word": [\n        {\n          Definition: "Timid means to be shy or easily frightened.",\n          "Translated Word": "Tímido significa ser tímido o asustarse fácilmente.",\n          Word: "Timid",\n        }, {\n          Definition: "Mumbled means to speak quietly and unclearly.",\n          "Translated Word": "Murmuró significa hablar en voz baja y poco clara.",\n          Word: "Mumbled",\n        }, {\n          Definition: "Squeaked means to make a short, high-pitched sound.",\n          "Translated Word": "Chirrido significa hacer un sonido corto y agudo.",\n          Word: "Squeaked",\n        }, {\n          Definition: "Kindness means being friendly, generous, and helpful.",\n          "Translated Word": "Amabilidad significa ser amigable, generoso y servicial.",\n          Word: "Kindness",\n        }\n      ],\n    },\n    Title: "Tapioca\'s Big Discovery",\n    "Two Sentence Summary": "Tapioca, a shy Sumikko Gurashi toy, feels too small to join the other toys\' games. However, when a teddy bear loses his button, Tapioca discovers that even small acts of kindness can make a big difference.",\n  },\n}"',
});

// New model for personality guessing
const personalityModel = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction:
    'You are a creative toy personality expert who can imagine the personality traits and characteristics of toys based on their name and type. You create engaging, child-friendly personality profiles that are imaginative and positive.',
});

const translationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 8192,
  responseMimeType: 'application/json',
  responseSchema: {
    type: 'object',
    properties: {
      Story: {
        type: 'object',
        properties: {
          'Page Contents': {
            type: 'array',
            items: {
              type: 'string',
            },
          },
          'Two Sentence Summary': {
            type: 'string',
          },
          'Life Lesson': {
            type: 'string',
          },
          Title: {
            type: 'string',
          },
        },
        required: [
          'Page Contents',
          'Two Sentence Summary',
          'Life Lesson',
          'Title',
          'Recommended Vocabulary Words',
        ],
      },
    },
    required: ['Story'],
  },
};

const personalityConfig = {
  temperature: 0.8,
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 2048,
  responseMimeType: 'application/json',
  responseSchema: {
    type: 'object',
    properties: {
      Personality: {
        type: 'object',
        properties: {
          Traits: {
            type: 'array',
            items: {
              type: 'string',
            },
            description: '5 key personality traits of the toy',
          },
          Backstory: {
            type: 'string',
            description: 'A brief backstory for the toy (2-3 sentences)',
          },
          Likes: {
            type: 'array',
            items: {
              type: 'string',
            },
            description: '3 things the toy likes',
          },
          Dislikes: {
            type: 'array',
            items: {
              type: 'string',
            },
            description: '2 things the toy dislikes',
          },
          'Special Ability': {
            type: 'string',
            description: 'A special ability or talent the toy has',
          },
        },
        required: ['Traits', 'Backstory', 'Likes', 'Dislikes', 'Special Ability'],
      },
    },
    required: ['Personality'],
  },
};

export async function storyTranslation(language, json) {
  const chatSession = translationModel.startChat({
    generationConfig: translationConfig,
    history: [
      {
        role: 'user',
        parts: [{ text: language }],
      },
    ],
  });

  const result = await chatSession.sendMessage(json);
  return result.response.text();
}

export async function guessPersonality(toyName, toyType) {
  try {
    const prompt = `Create a personality profile for a toy named "${toyName}" which is a ${toyType}. 
      Imagine what kind of personality traits, likes, dislikes, and special abilities this toy might have.
      Be creative, child-friendly, and positive. The personality should be engaging for children.`;

    const result = await personalityModel.generateContent({
      contents: [{ role: 'user', parts: [{ text: prompt }] }],
      generationConfig: personalityConfig,
    });

    const response = result.response;
    return response.text();
  } catch (error) {
    console.error('Error generating toy personality:', error);
    throw error;
  }
}
