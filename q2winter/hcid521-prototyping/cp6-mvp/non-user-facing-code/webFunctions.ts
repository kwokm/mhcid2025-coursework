import { exec } from 'child_process';
import * as readline from 'readline';
import * as fs from 'fs'; // File system module

// Update JSON file from AI output
export function updateAudioFiles(jsonString: string) {
    try {
        // Parse the JSON string
        const data = JSON.parse(jsonString);

        // Write the jsonString to currentResponse.json
        fs.writeFile('currentResponse.json', jsonString, (writeErr: any) => {
            if (writeErr) {
                console.error('Error writing to currentResponse.json:', writeErr);
            } else {
                console.log('currentResponse.json updated successfully.');
            }
        });

    } catch (error: any) {
        console.error('Error updating audio files:', error.message);
    }
}