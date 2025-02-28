import { wordsToAudio } from "./wordsToAudioGeminiPrompt";
import { startListening, updateAudioFiles } from "./buttonactionKeyboard";
async function main() {
    const result = await wordsToAudio("Spanish: tiger, bear, cat, dog");
    console.log(result.response);
    updateAudioFiles(result.response.text());
    startListening();
}

main();