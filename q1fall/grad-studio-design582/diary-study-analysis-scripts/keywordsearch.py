import os
from collections import Counter
import nltk
from nltk.corpus import stopwords
import string
import re

# Download required NLTK data (run once)
nltk.download('stopwords')

# Define keywords and phrases to search for
SEARCH_TERMS = {
    'keywords': [
        'python',
        'data',
        'analysis',
        # Add more single keywords here
    ],
    'phrases': [
        'machine learning',
        'data science',
        'artificial intelligence',
        # Add more phrases here
    ]
}

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def count_keywords_and_phrases(text, search_terms):
    counts = Counter()
    cleaned_text = clean_text(text)
    
    # Count single keywords
    words = cleaned_text.split()
    for keyword in search_terms['keywords']:
        keyword = keyword.lower()
        counts[keyword] = sum(1 for word in words if word == keyword)
    
    # Count phrases
    for phrase in search_terms['phrases']:
        phrase = phrase.lower()
        # Use regex to count overlapping matches
        count = len(re.findall(f'(?={phrase})', cleaned_text))
        if count > 0:
            counts[phrase] = count
            
    return counts

def process_file(filepath, search_terms):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        return count_keywords_and_phrases(text, search_terms)
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return Counter()

def analyze_transcripts(directory, search_terms):
    total_counts = Counter()
    
    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            print(f"Processing {filename}...")
            file_counts = process_file(filepath, search_terms)
            total_counts.update(file_counts)
    
    return total_counts

def print_results(counts):
    if not counts:
        print("No matches found.")
        return
        
    print("\nResults:")
    print("-" * 40)
    
    # Sort by count (highest first)
    for term, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"{term}: {count}")

def main():
    directory = "RawTranscripts"
    
    # Verify directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found!")
        return
    
    print(f"Analyzing files in {directory}...")
    word_counts = analyze_transcripts(directory, SEARCH_TERMS)
    print_results(word_counts)

if __name__ == "__main__":
    main()