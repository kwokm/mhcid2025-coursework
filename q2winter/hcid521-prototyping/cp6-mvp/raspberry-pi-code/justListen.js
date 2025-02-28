import { wordsToAudio } from "./gemini-prompts-js/wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles, initializeAudioFiles } from "./buttonactionKeyboard";
async function main() {

    initializeAudioFiles();
    startListening();

}

main();