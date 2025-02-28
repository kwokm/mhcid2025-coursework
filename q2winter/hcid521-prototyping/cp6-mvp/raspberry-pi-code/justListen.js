import { wordsToAudio } from "./wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles, initializeAudioFiles } from "./buttonactionKeyboard";
async function main() {

    initializeAudioFiles();
    startListening();

}

main();