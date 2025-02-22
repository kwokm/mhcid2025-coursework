import os
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string
from nltk.corpus import brown

# Download required NLTK data (run once)
nltk.download('stopwords')
nltk.download('brown')

def add_custom_stopwords(additional_words):
    """
    Add custom words to the stopwords set.
    Args:
        additional_words (list or set): Collection of words to add as stopwords
    """
    stop_words = set(stopwords.words('english'))
    stop_words.update(additional_words)
    return stop_words

def get_english_frequencies():
    """
    Calculate word frequencies from the Brown corpus as a baseline for English language.
    Returns a dictionary of words and their frequencies per million words.
    """
    words = [word.lower() for word in brown.words()]
    total_words = len(words)
    word_freq = Counter(words)
    # Convert to frequency per million
    return {word: (count/total_words)*1000000 for word, count in word_freq.items()}

def process_file(filepath, custom_stops=None):
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words
    words = text.split()
    
    # Get English stop words with custom additions
    if custom_stops is None:
        custom_stops = {'n/a', 'etc', 'na', 'would', 'could', 'should', 'said'}
    
    stop_words = add_custom_stopwords(custom_stops)
    
    # Filter out stop words and count remaining words
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_counts = Counter(filtered_words)
    
    # After creating word_counts, calculate words per million
    total_words = sum(word_counts.values())
    word_frequencies = {word: (count/total_words)*1000000 
                       for word, count in word_counts.items()}
    return word_counts, word_frequencies

def analyze_transcripts(directory, custom_stops=None):
    total_counts = Counter()
    total_frequencies = {}
    
    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            file_counts, file_frequencies = process_file(filepath, custom_stops)
            total_counts.update(file_counts)
            # Combine frequencies (taking the average)
            for word, freq in file_frequencies.items():
                if word in total_frequencies:
                    total_frequencies[word] = (total_frequencies[word] + freq) / 2
                else:
                    total_frequencies[word] = freq
    
    return total_counts, total_frequencies

def main():
    # Define custom stopwords here
    custom_stops = {'n/a', 'etc', 'na', 'would', 'could', 'should', 'said'}
    # Add any additional stopwords
    more_stops = {'feel', 'like', 'think', 'felt', 'also', 'would', 'made'}
    custom_stops.update(more_stops)
    
    directory = "TranscriptsNoSenses"
    
    # Get baseline English frequencies
    english_frequencies = get_english_frequencies()
    
    # Get transcript word counts and frequencies
    word_counts, transcript_frequencies = analyze_transcripts(directory, custom_stops)
    
    # Create AnalysisResults directory if it doesn't exist
    os.makedirs("AnalysisResults", exist_ok=True)
    
    # Save results to CSV with frequency comparison
    output_file = os.path.join("AnalysisResults", "word_counts_frequency.csv")
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        from csv import writer
        csv_writer = writer(csvfile)
        csv_writer.writerow(['Word', 'Count', 'Frequency_per_Million', 'English_Baseline_Frequency', 'Relative_Usage'])
        
        for word, count in word_counts.most_common():
            transcript_freq = transcript_frequencies.get(word, 0)
            english_freq = english_frequencies.get(word, 0)
            relative_usage = 'N/A' if english_freq == 0 else f"{transcript_freq/english_freq:.2f}x"
            
            csv_writer.writerow([
                word,
                count,
                f"{transcript_freq:.2f}",
                f"{english_freq:.2f}",
                relative_usage
            ])
    
    print(f"Results have been saved to {output_file}")

if __name__ == "__main__":
    main()