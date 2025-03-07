import { wordsToAudio, storyCreation } from "../gemini-prompts/index";
import { startListening, updateAudioFiles } from "./buttonactionKeyboard";
async function main() {    
    const result = await wordsToAudio("Chinese: robot, tiger, lightsaber, cat");
    console.log("prompting gemini to match toys with audio files");
    console.log("prompt: Chinese: robot, tiger, lightsaber, cat")
    console.log(result.response.text());
    updateAudioFiles(result.response.text());
    storyCreation("growly the tiger");
    startListening();
}

main();