import { wordsToAudio } from './gemini-prompts/wordsToAudioGeminiPrompt';
import { startListening, updateAudioFiles } from './ARCHIVE_jscode/buttonactionKeyboard';
async function main() {
  const result = await wordsToAudio('Chinese: robot, tiger, lightsaber, cat');
  console.log(result.response.text());
  updateAudioFiles(result.response.text());
  startListening();
}

main();
