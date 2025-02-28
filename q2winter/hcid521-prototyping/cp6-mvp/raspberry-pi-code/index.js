import { wordsToAudio } from "./gemini-prompts-js/wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles } from "./buttonactionKeyboard";
async function main() {    
    const result = await wordsToAudio("Spanish: tiger, bear, cat, dog");
    console.log(result.response.text());
    updateAudioFiles(result.response.text());
    startListening();
}

main();