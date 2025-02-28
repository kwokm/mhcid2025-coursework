import { wordsToAudio } from "./wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles } from "./raspberryPiCode/buttonactionKeyboard";
async function main() {

    
    startListening();

}

main();