import * as utils from './index';
import * as geminiPrompts from '../raspberry-pi-code/gemini-prompts/index';

const sampleImagePath =
  '/Users/michaelkwok/Code/mhcid2025-coursework/q2winter/hcid521-prototyping/cp6-mvp/non-user-facing-code/sampleImage.jpg';
const sampleImageType = utils.getMimeType(sampleImagePath);
const language = 'Spanish';

async function main() {
  // AI Prompt 1 - Toy Identification
  const toyIdentification = await geminiPrompts.identifyToy(sampleImagePath, sampleImageType, '');
  console.log('AI Prompt 1 - Toy Identification Input: ', sampleImagePath);
  console.log('AI Prompt 1 - Toy Identification Output: ', JSON.parse(toyIdentification));
  console.log('\n');

  // Preparing inputs for AI Prompt 2 - Story Creation
  const toyName = utils.extractJsonValues('Name', JSON.parse(toyIdentification));
  const toyType = utils.extractJsonValues('Item', JSON.parse(toyIdentification));

  // AI Prompt 2 - Story Creation
  console.log('AI Prompt 2 - Story Creation Input: ', toyName + ' the ' + toyType);
  const storyCreation = await geminiPrompts.storyCreation(toyName + ', ' + toyType);
  console.log('AI Prompt 2 - Story Creation Output: ', JSON.parse(storyCreation));
  console.log('\n');

  // Preparing inputs for AI Prompt 3 - Story Translation
  const storyCondensed = utils
    .extractJsonValues('Page Contents', JSON.parse(storyCreation))
    .join(' ');

  // AI Prompt 3 - Choose Vocabulary
  const chooseVocabulary = await geminiPrompts.chooseVocabulary(storyCondensed);
  console.log('AI Prompt 3 - Choose Vocabulary Input: ', storyCondensed);
  console.log('AI Prompt 3 - Choose Vocabulary Output: ', JSON.parse(chooseVocabulary));
  console.log('\n');

  // Preparing inputs for AI Prompt 4 - vocab translation & audio file finding
  const vocabularyWords = utils.extractJsonValues('Word', JSON.parse(chooseVocabulary)).join(', ');

  // AI Prompt 4 - vocab translation & audio file finding
  console.log(
    'AI Prompt 4 - vocab translation & audio file finding Input: ',
    language + ': ' + vocabularyWords
  );
  const finalOutput = await geminiPrompts.wordsToAudio(language + ': ' + vocabularyWords);
  console.log(
    'AI Prompt 4 - vocab translation & audio file finding Output: ',
    JSON.parse(finalOutput)
  );
  console.log('\n');
  utils.updateAudioFiles(finalOutput);
  console.log('JSON file ready for soundboard creation.');
}

main();
