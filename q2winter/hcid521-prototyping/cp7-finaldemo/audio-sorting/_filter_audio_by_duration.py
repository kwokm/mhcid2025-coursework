import os
import wave
import shutil

def filter_audio_by_duration(folder_path, output_folder, min_duration=0.25, max_duration=5.5):
    """
    Recursively scans a folder and its subdirectories for WAV files.
    Moves files that are shorter than min_duration or longer than max_duration to the output folder.

    Args:
        folder_path (str): The path to the root folder.
        output_folder (str): The folder where files outside the duration range will be moved.
        min_duration (float): Minimum duration in seconds. Defaults to 0.3.
        max_duration (float): Maximum duration in seconds. Defaults to 5.0.
    """
    moved_count = 0
    processed_count = 0
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if not filename.lower().endswith('.wav'):
                    continue
                    
                file_path = os.path.join(root, filename)
                processed_count += 1
                
                try:
                    # Get audio duration using wave module
                    with wave.open(file_path, 'rb') as wf:
                        # Duration = frames / framerate
                        duration = wf.getnframes() / wf.getframerate()
                    
                    # Check if file should be moved
                    if duration < min_duration or duration > max_duration:
                        # Create a subfolder structure in the output folder that mirrors the input folder
                        rel_path = os.path.relpath(file_path, folder_path)
                        dest_path = os.path.join(output_folder, rel_path)
                        
                        # Create parent directories if they don't exist
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        
                        # Move the file
                        shutil.move(file_path, dest_path)
                        moved_count += 1
                        print(f"Moved: {file_path} → {dest_path} (Duration: {duration:.2f}s)")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        
        print(f"\nProcessing complete!")
        print(f"Processed {processed_count} WAV files")
        print(f"Moved {moved_count} files outside duration range ({min_duration}s - {max_duration}s) to {output_folder}")
                    
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    folder_path = "./allnew/"  # Replace with the actual folder path
    output_folder = "./allnewDurationFiltered/"  # Folder where files outside duration range will be moved
    filter_audio_by_duration(folder_path, output_folder) 