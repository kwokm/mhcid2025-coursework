import * as utils from "./index";
import * as geminiPrompts from "../raspberry-pi-code/gemini-prompts/index";

const sampleImagePath = "/Users/michaelkwok/Code/mhcid2025-coursework/q2winter/hcid521-prototyping/cp6-mvp/non-user-facing-code/sampleImage.jpg";
const sampleImageType = utils.getMimeType(sampleImagePath);
const language = "Spanish";

async function main() {    
    // AI Prompt 1 - Toy Identification
    const toyIdentification = await geminiPrompts.identifyToy(sampleImagePath, sampleImageType, "");
    console.log("AI Prompt 1 - Toy Identification Input: ", sampleImagePath);
    console.log("AI Prompt 1 - Toy Identification Output: ", JSON.parse(toyIdentification));
    console.log('\n');

    // Preparing inputs for AI Prompt 2 - Story Creation
    const toyName = utils.extractJsonValues("Name", JSON.parse(toyIdentification));
    const toyType = utils.extractJsonValues("Item", JSON.parse(toyIdentification));

    // AI Prompt 2 - Story Creation
    console.log("AI Prompt 2 - Story Creation Input: ", toyName + " the " + toyType + ", " + language);
    const storyCreation = await geminiPrompts.storyCreation(toyName + ", " + toyType + ", " + language);
    console.log("AI Prompt 2 - Story Creation Output: ", JSON.parse(storyCreation));
    console.log('\n');

    // Preparing inputs for AI Prompt 3 - audio file finding
    const vocabularyWords = utils.extractJsonValues("Word", JSON.parse(storyCreation));

    // AI Prompt 3 - audio file finding
    console.log("AI Prompt 3 - audio file finding Input: ", language + ": " + vocabularyWords.join(", "));
    const finalOutput = await geminiPrompts.wordsToAudio(language + ": " + vocabularyWords.join(", "));
    console.log("AI Prompt 3 - Story Translation Output: ", JSON.parse(finalOutput));
    console.log('\n');
    utils.updateAudioFiles(finalOutput);
    console.log("JSON file ready for soundboard creation.");
}

main();