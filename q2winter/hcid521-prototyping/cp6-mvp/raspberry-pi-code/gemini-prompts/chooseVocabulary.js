const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require('@google/generative-ai');

const apiKey = 'AIzaSyD1rgVz8vdJRIzpYOtrR6wWQmk3M1OI2iE';
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction:
    'This is part of a prompt chain helping bilingual parents connect with their children and teach them new words. You will receive a story in markdown format.\n\nChoose 4 words from the story for the child to learn. The words should be appropriate for the reading level of 3-6 years old. Add a description on how to pronounce the word while providing a mental model to allow parents to teach their kid to easily remember the word. Make sure to specify "description". Make sure the tense in the story and the chosen words are the same tense because the children this age are not old enough to learn grammar yet.  Generate 20 backups for 24 total.',
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
      'Word List': {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            Word: {
              type: 'string',
            },
            Pronounciation: {
              type: 'string',
            },
            Definition: {
              type: 'string',
            },
          },
          required: ['Word', 'Pronounciation', 'Definition'],
        },
      },
    },
    required: ['Word List'],
  },
};

export async function chooseVocabulary(story) {
  const chatSession = model.startChat({
    generationConfig,
    history: [],
  });

  const result = await chatSession.sendMessage(story);
  return result.response.text();
}
