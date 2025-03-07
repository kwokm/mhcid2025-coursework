import * as geminiPrompts from "../raspberry-pi-code/gemini-prompts/index.js";
import * as utils from "./utilityFunctions.js";

async function main() {
    const result = await geminiPrompts.storyCreation("Growly the Tiger, Spanish");
    console.log(result);
    const jsonResult = JSON.parse(result);
    const extracted = utils.extractJsonValues("Definition", jsonResult);
    console.log(extracted);
}

main();
