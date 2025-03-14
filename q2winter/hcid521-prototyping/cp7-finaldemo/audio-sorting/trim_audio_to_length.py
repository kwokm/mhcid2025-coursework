import os
from pydub import AudioSegment

def trim_audio_to_length(folder_path, target_duration=4.0):
    """
    Recursively scans a folder and its subdirectories for WAV files.
    Trims all files to the specified duration (in seconds).
    If a file is shorter than the target duration, it is left unchanged.

    Args:
        folder_path (str): The path to the root folder.
        target_duration (float): Target duration in seconds. Defaults to 3.0.
    """
    processed_count = 0
    trimmed_count = 0
    
    try:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if not filename.lower().endswith('.wav'):
                    continue
                    
                file_path = os.path.join(root, filename)
                processed_count += 1
                
                try:
                    # Load audio file
                    audio = AudioSegment.from_wav(file_path)
                    
                    # Calculate duration in milliseconds
                    duration_ms = len(audio)
                    target_duration_ms = int(target_duration * 1000)
                    
                    # Only trim if the file is longer than target duration
                    if duration_ms > target_duration_ms:
                        # Trim to target duration (keep the first part)
                        trimmed_audio = audio[:target_duration_ms]
                        
                        # Apply a short fade out at the end (50ms) for a smoother sound
                        trimmed_audio = trimmed_audio.fade_out(50)
                        
                        # Export back to the same file
                        trimmed_audio.export(file_path, format="wav")
                        
                        trimmed_count += 1
                        print(f"Trimmed: {file_path} ({duration_ms/1000:.2f}s → {target_duration:.2f}s)")
                
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        print(f"\nProcessing complete!")
        print(f"Processed {processed_count} WAV files")
        print(f"Trimmed {trimmed_count} files to {target_duration} seconds")
                    
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    folder_path = "./"  # Replace with the actual folder path
    trim_audio_to_length(folder_path) 