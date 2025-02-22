import os
import pandas as pd
from textblob import TextBlob
import sys

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Classify sentiment
    if analysis.sentiment.polarity > 0:
        return 'Positive', analysis.sentiment.polarity
    elif analysis.sentiment.polarity < 0:
        return 'Negative', analysis.sentiment.polarity
    else:
        return 'Neutral', analysis.sentiment.polarity

# Check if directory path is provided
if len(sys.argv) != 2:
    print("Usage: python sentimentanalysis.py <directory_path>")
    sys.exit(1)

directory_path = sys.argv[1]

# Check if directory exists
if not os.path.isdir(directory_path):
    print(f"Error: Directory '{directory_path}' does not exist")
    sys.exit(1)

# Create AnalysisResults directory if it doesn't exist
results_dir = 'AnalysisResults'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Prepare the DataFrame to store results
results = []

# Iterate through all .txt files in the specified directory
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire file content
            text_content = file.read()
            sentiment, score = analyze_sentiment(text_content.strip())
            results.append({'File': filename, 'Sentiment': sentiment, 'Score': score})

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save to a CSV file in the AnalysisResults directory
output_filename = os.path.join(results_dir, 'sentiment_analysis_results.csv')
df.to_csv(output_filename, index=False)

print(f'Sentiment analysis completed. Results saved to {output_filename}.')
