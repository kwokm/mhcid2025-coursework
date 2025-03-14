import os
import wave
import shutil
import numpy as np
from scipy.io import wavfile

def copy_and_trim_audio(source_folder, destination_folder, min_duration=0.25, max_duration=5.5, trim_length=3.5):
    """
    Recursively scans a folder for WAV files, copies and trims only files 
    that are longer than max_duration.
    Files shorter than or equal to max_duration are skipped.

    Args:
        source_folder (str): The path to the source folder containing WAV files.
        destination_folder (str): The folder where processed files will be saved.
        min_duration (float): Minimum acceptable duration in seconds (not used for filtering, kept for API consistency).
        max_duration (float): Maximum duration in seconds. Only files longer than this will be processed.
        trim_length (float, optional): Length in seconds to trim audio files to. If None, uses max_duration.
    """
    # If trim_length is not specified, use max_duration
    if trim_length is None:
        trim_length = max_duration
        
    trimmed_count = 0
    skipped_count = 0
    processed_count = 0
    
    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    
    try:
        for root, _, files in os.walk(source_folder):
            for filename in files:
                if not filename.lower().endswith('.wav'):
                    continue
                    
                source_path = os.path.join(root, filename)
                processed_count += 1
                
                try:
                    # First, get audio duration
                    with wave.open(source_path, 'rb') as wf:
                        sample_rate = wf.getframerate()
                        n_frames = wf.getnframes()
                        duration = n_frames / sample_rate
                    
                    # Only process files longer than max_duration
                    if duration > max_duration:
                        # Get relative path to maintain folder structure
                        rel_path = os.path.relpath(source_path, source_folder)
                        dest_path = os.path.join(destination_folder, rel_path)
                        
                        # Create parent directories if they don't exist
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        
                        # Copy the file first
                        shutil.copy2(source_path, dest_path)
                        
                        # Read the audio file
                        sample_rate, audio_data = wavfile.read(dest_path)
                        
                        # Calculate how many samples to keep
                        samples_to_keep = int(trim_length * sample_rate)
                        
                        # Trim the audio data
                        trimmed_data = audio_data[:samples_to_keep]
                        
                        # Write the trimmed audio back to the destination file
                        wavfile.write(dest_path, sample_rate, trimmed_data)
                        
                        trimmed_count += 1
                        print(f"Copied and trimmed: {source_path} → {dest_path} (Original: {duration:.2f}s, Trimmed: {trim_length:.2f}s)")
                    else:
                        skipped_count += 1
                        print(f"Skipped: {source_path} (Duration: {duration:.2f}s is within limit)")
                        
                except Exception as e:
                    print(f"Error processing {source_path}: {e}")
        
        print(f"\nProcessing complete!")
        print(f"Processed {processed_count} WAV files")
        print(f"Trimmed {trimmed_count} files longer than {max_duration}s to {trim_length}s")
        print(f"Skipped {skipped_count} files that didn't need trimming")
                    
    except FileNotFoundError:
        print(f"Error: Folder '{source_folder}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    source_folder = "./allnewDurationFiltered/"  # Replace with the actual source folder path
    destination_folder = "./allnewTrimmed/"  # Folder where processed files will be saved
    
    # Example: Process files longer than 5.5s but trim them to 3.0s
    copy_and_trim_audio(source_folder, destination_folder, max_duration=5.5, trim_length=3.5)
    
    # If you want to use the same value for both (original behavior):
    # copy_and_trim_audio(source_folder, destination_folder) 