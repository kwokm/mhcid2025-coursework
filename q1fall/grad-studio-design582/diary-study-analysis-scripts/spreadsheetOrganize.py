import os

def process_raw_transcript(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content by the delimiter ("|" surrounded by newlines)
    # Using strip() to remove any leading/trailing whitespace
    entries = [entry.strip() for entry in content.split('\n|\n')]
    
    # Write to CSV
    import csv
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write each entry as a row
        for entry in entries:
            writer.writerow([entry])

def process_all_transcripts(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each txt file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.txt', '.csv'))
            process_raw_transcript(input_path, output_path)

# Example usage
process_all_transcripts('RawTranscripts', 'processed')