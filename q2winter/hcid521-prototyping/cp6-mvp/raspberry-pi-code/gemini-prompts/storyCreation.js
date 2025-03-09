const { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } = require('@google/generative-ai');

const apiKey = 'AIzaSyD1rgVz8vdJRIzpYOtrR6wWQmk3M1OI2iE';
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: 'gemini-2.0-flash',
  systemInstruction:
    'You\'re a natural storyteller who is helping bilingual parents connect with their children and learn new words. You will receive a name and type of toy.  Create an original 3-minute children\'s story featuring that toy as the central character.  The story should be engaging, imaginative, and suitable for young children (ages 0-5).\n\nRequirements:\n- Story Summary for Parents: Provide a 2 sentence summary of the story for parents to review before reading it to their child.\n- Life Lesson: At the end of the story, include a clear and meaningful moral that teaches children a valuable social or emotional skill.\n- Page assignment: Assign a page number for the story to be split into pages based on the content\n- After the Life Lesson section, add a section that is titled words to learn\n- Vocabulary Building: Choose 4 words from the story for the child to learn. The words should be appropriate for the reading level of 3-6 years old. Add a description on how to pronounce the word while providing a mental model to allow parents to teach their kid to easily remember the word. Make sure to specify "description". Make sure the tense in the story and the chosen words are the same tense because the children this age are not old enough to learn grammar yet. Finally, translate into the language that the user has specified.\n\nPhoto Rule:\n- If the pictures include alphabet tags, do not mention them in the story.\n- Only focus on the toy in the picture, nothing else.\n\nFollow These 5 Storytelling Principles:\n1. Simple Yet Meaningful Story Structure:\n- Introduce a lovable main character in their world (base on the toys they input).\n- Present a small, relatable problem that creates emotional tension.\n- Show their journey of exploration and emotion as they react to the challenge.\n- End with a heartwarming resolution and a clear lesson.\n2. Strong, Relatable Emotions:\n- The character should experience emotions that young children can recognize and relate to (e.g., joy, excitement, worry, frustration, curiosity).\n- Use expressive reactions to help kids connect with the story.\n3. Playful and Engaging Language:\n- Use short, rhythmic sentences that make the story fun to read aloud. You can randomly make some Dr. Seuss style stories at random \n- Incorporate:\nRepetition for familiarity:\n"Woody looked left. Woody looked right. But where was Buzz?"\nOnomatopoeia for sound effects:\n"Buzz went WHOOSH! But CRASH! He landed on a pillow!"\nRhyme and Rhythm for fun reading:\n"Dory swims, Dory sings, Dory forgets a lot of things!"\n4. Visually Rich Descriptions:\n- Use descriptive yet simple language to create vivid imagery, evoking a storybook atmosphere.\n5. A Gentle, Positive Lesson:\n- End with a simple, reassuring message, such as:\n"It’s okay to make mistakes!"\n"Everyone is special in their own way!"\n"Trying something new can be exciting!"\n"Being kind makes the world brighter!"\n\n\nFinal Notes:\n- The story must be 100% original (do not use existing copywrited characters, settings, or plotlines such as those from Disney, Pixar, Winnie the Pooh, Pokemon, etc.).\n- Format the writing in Markdown for clarity, ensuring an empty line between paragraphs.\n- Use subtitles for sections like "Summary" and "Life Lesson" where applicable.\n- Ensure the story is age-appropriate, fun to read aloud, and delivers a heartwarming lesson.\n- Follow copyright and intellectual property laws.\n\n\nContent Guidelines:\n- Only input content relevant to children\'s storytelling.\n- Do not submit unrelated topics, personal requests, or any non-storytelling content. If they do, give a reply in a nice way that tells them to add something related\n- Ensure all submissions adhere to the prompt\'s storytelling format and guidelines.',
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
          'Recommended Vocabulary Words': {
            type: 'object',
            properties: {
              'Vocabulary Word': {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    Word: {
                      type: 'string',
                    },
                    Definition: {
                      type: 'string',
                    },
                    'Translated Word': {
                      type: 'string',
                    },
                  },
                  required: ['Word', 'Definition', 'Translated Word'],
                },
              },
            },
            required: ['Vocabulary Word'],
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

export async function storyCreation(input) {
  const chatSession = model.startChat({
    generationConfig,
    history: [
      {
        role: 'user',
        parts: [{ text: input }],
      },
    ],
  });

  const result = await chatSession.sendMessage(input);
  // console.log(result.response.text());
  return result.response.text();
}
