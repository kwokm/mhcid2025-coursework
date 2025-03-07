import { wordsToAudio } from "../gemini-prompts/wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles, initializeAudioFiles } from "./buttonactionKeyboard";
async function main() {

    initializeAudioFiles();
    startListening();

}

main();