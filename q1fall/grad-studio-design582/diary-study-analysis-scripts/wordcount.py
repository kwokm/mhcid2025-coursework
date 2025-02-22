import os
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string

# Download required NLTK data (run once)
nltk.download('stopwords')

def add_custom_stopwords(additional_words):
    """
    Add custom words to the stopwords set.
    Args:
        additional_words (list or set): Collection of words to add as stopwords
    """
    stop_words = set(stopwords.words('english'))
    stop_words.update(additional_words)
    return stop_words

def process_file(filepath):
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words
    words = text.split()
    
    # Get English stop words with custom additions
    custom_stops = {'n/a', 'etc', 'na', 'would', 'could', 'should', 'said'}  # Extended default list
    stop_words = add_custom_stopwords(custom_stops)
    
    # Filter out stop words and count remaining words
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_counts = Counter(filtered_words)
    
    return word_counts

def analyze_transcripts(directory):
    total_counts = Counter()
    
    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            file_counts = process_file(filepath)
            total_counts.update(file_counts)
    
    return total_counts

def main():
    # Add any additional stopwords
    more_stops = {'feel', 'like', 'think', 'felt', 'also', 'would', 'made'}
    custom_stops.update(more_stops)
    
    directory = "RawTranscripts"
    word_counts = analyze_transcripts(directory)
    
    # Create AnalysisResults directory if it doesn't exist
    os.makedirs("AnalysisResults", exist_ok=True)
    
    # Save results to CSV
    output_file = os.path.join("AnalysisResults", "word_counts.csv")
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        from csv import writer
        csv_writer = writer(csvfile)
        csv_writer.writerow(['Word', 'Count'])  # Header
        csv_writer.writerows(word_counts.most_common())
    
    print(f"Results have been saved to {output_file}")

if __name__ == "__main__":
    main()