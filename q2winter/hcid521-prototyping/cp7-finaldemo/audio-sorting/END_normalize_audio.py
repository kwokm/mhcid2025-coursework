import os
import wave
import numpy as np
import argparse
from scipy.io import wavfile

def normalize_audio(input_folder, output_folder, target_level=0.5, min_length=0.0, max_length=float('inf')):
    """
    Normalize audio files to a target amplitude level.
    
    Args:
        input_folder (str): Path to folder containing audio files
        output_folder (str): Path to save normalized audio files
        target_level (float): Target amplitude level between 0 and 1 (default: 0.5, 50% of max amplitude)
        min_length (float): Skip files shorter than this (in seconds)
        max_length (float): Skip files longer than this (in seconds)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Counters for reporting
    processed_count = 0
    skipped_count = 0
    normalized_count = 0
    
    print(f"Normalizing audio files to {target_level*100:.1f}% amplitude level...")
    
    # Process all files in the input folder (and subfolders)
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if not filename.lower().endswith('.wav'):
                continue
                
            file_path = os.path.join(root, filename)
            processed_count += 1
            
            try:
                # Check file duration
                with wave.open(file_path, 'rb') as wf:
                    sample_rate = wf.getframerate()
                    n_frames = wf.getnframes()
                    duration = n_frames / sample_rate
                
                # Skip files outside the length range
                if duration < min_length or duration > max_length:
                    print(f"Skipped: {file_path} (Duration: {duration:.2f}s outside range {min_length}s - {max_length}s)")
                    skipped_count += 1
                    continue
                
                # Read the audio file
                sample_rate, audio_data = wavfile.read(file_path)
                
                # Get relative path to maintain folder structure
                rel_path = os.path.relpath(file_path, input_folder)
                output_path = os.path.join(output_folder, rel_path)
                
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Convert to float for processing
                audio_type = audio_data.dtype
                if audio_type != np.float32 and audio_type != np.float64:
                    audio_float = audio_data.astype(np.float32)
                    max_possible_value = np.iinfo(audio_type).max
                    audio_float = audio_float / max_possible_value
                else:
                    audio_float = audio_data
                
                # Calculate current peak amplitude
                if len(audio_float.shape) > 1:  # Stereo
                    peak_amplitude = np.max(np.abs(audio_float))
                else:  # Mono
                    peak_amplitude = np.max(np.abs(audio_float))
                
                # Calculate normalization factor
                if peak_amplitude > 0:
                    normalization_factor = target_level / peak_amplitude
                else:
                    normalization_factor = 1.0
                
                # Apply normalization
                normalized_audio = audio_float * normalization_factor
                
                # Convert back to original data type
                if audio_type != np.float32 and audio_type != np.float64:
                    normalized_audio = (normalized_audio * max_possible_value).astype(audio_type)
                
                # Save normalized audio
                wavfile.write(output_path, sample_rate, normalized_audio)
                
                normalized_count += 1
                print(f"Normalized: {file_path} → {output_path}")
                print(f"  Original peak: {peak_amplitude:.6f}")
                print(f"  New peak: {min(target_level, 1.0):.6f}")
                print(f"  Scale factor: {normalization_factor:.6f}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                skipped_count += 1
    
    print(f"\nProcessing complete!")
    print(f"Processed {processed_count} files")
    print(f"Normalized {normalized_count} files to {target_level*100:.1f}% amplitude")
    print(f"Skipped {skipped_count} files")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize audio files to a target amplitude level")
    parser.add_argument("input_folder", help="Folder containing audio files to normalize")
    parser.add_argument("--output_folder", default="./normalized_audio", help="Folder to save normalized audio files")
    parser.add_argument("--target_level", type=float, default=0.5, help="Target amplitude level 0-1 (default: 0.5, 50%% of max)")
    parser.add_argument("--min_length", type=float, default=0.0, help="Skip files shorter than this (in seconds)")
    parser.add_argument("--max_length", type=float, default=float('inf'), help="Skip files longer than this (in seconds)")
    
    args = parser.parse_args()
    
    # Ensure target level is between 0 and 1
    target_level = max(0.0, min(1.0, args.target_level))
    
    normalize_audio(
        args.input_folder, 
        args.output_folder, 
        target_level,
        args.min_length,
        args.max_length
    ) 