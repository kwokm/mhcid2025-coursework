#!/bin/bash

# GitHub repository details
OWNER="kwokm"
REPO="mhcid2025-coursework"
BRANCH="main"
PATH_IN_REPO="q2winter/hcid521-prototyping/cp6-mvp/raspberry-pi-code"
OUTPUT_DIR="."  # Changed to current directory

echo "Starting download of GitHub repository folder:"
echo "Repository: $OWNER/$REPO"
echo "Branch: $BRANCH"
echo "Path: $PATH_IN_REPO"
echo "Output directory: Current directory"
echo "-------------------------------------------"

# Get the contents of the directory from GitHub API
API_URL="https://api.github.com/repos/$OWNER/$REPO/contents/$PATH_IN_REPO?ref=$BRANCH"
echo "Fetching directory listing from: $API_URL"

# Download the directory listing
CONTENTS=$(curl -s "$API_URL")

# Check if the API call was successful
if [[ "$CONTENTS" == *"Not Found"* ]] || [[ "$CONTENTS" == *"Bad credentials"* ]]; then
    echo "Error: Failed to fetch directory contents. Response:"
    echo "$CONTENTS"
    exit 1
fi

# Extract file information and download each file
echo "$CONTENTS" | grep -o '"path":"[^"]*","name":"[^"]*","download_url":"[^"]*"' | while read -r item; do
    # Extract path, name, and download_url
    PATH=$(echo "$item" | sed 's/.*"path":"\([^"]*\)".*/\1/')
    NAME=$(echo "$item" | sed 's/.*"name":"\([^"]*\)".*/\1/')
    URL=$(echo "$item" | sed 's/.*"download_url":"\([^"]*\)".*/\1/')
    
    # Skip if URL is null (likely a directory)
    if [[ "$URL" == "null" ]]; then
        continue
    fi
    
    # Create relative path for the file
    REL_PATH=${PATH#$PATH_IN_REPO/}
    OUTPUT_PATH="$OUTPUT_DIR/$NAME"
    
    echo "Downloading: $NAME"
    curl -s -L -o "$OUTPUT_PATH" "$URL"
    echo "Saved to: $OUTPUT_PATH"
done

# Handle subdirectories by recursively calling the GitHub API
process_directory() {
    local dir_path="$1"
    local output_subdir="$2"
    
    # Create the output subdirectory
    mkdir -p "$output_subdir"
    
    # Get the contents of the directory from GitHub API
    local api_url="https://api.github.com/repos/$OWNER/$REPO/contents/$dir_path?ref=$BRANCH"
    echo "Fetching subdirectory contents: $dir_path"
    
    # Download the directory listing
    local contents=$(curl -s "$api_url")
    
    # Process each item in the directory
    echo "$contents" | grep -o '"type":"[^"]*","name":"[^"]*"' | while read -r item; do
        # Extract type and name
        local type=$(echo "$item" | sed 's/.*"type":"\([^"]*\)".*/\1/')
        local name=$(echo "$item" | sed 's/.*"name":"\([^"]*\)".*/\1/')
        
        if [[ "$type" == "dir" ]]; then
            # Process subdirectory recursively
            process_directory "$dir_path/$name" "$output_subdir/$name"
        fi
    done
    
    # Download files in this directory
    echo "$contents" | grep -o '"path":"[^"]*","name":"[^"]*","download_url":"[^"]*"' | while read -r item; do
        # Extract path, name, and download_url
        local path=$(echo "$item" | sed 's/.*"path":"\([^"]*\)".*/\1/')
        local name=$(echo "$item" | sed 's/.*"name":"\([^"]*\)".*/\1/')
        local url=$(echo "$item" | sed 's/.*"download_url":"\([^"]*\)".*/\1/')
        
        # Skip if URL is null (likely a directory)
        if [[ "$url" == "null" ]]; then
            continue
        fi
        
        local output_path="$output_subdir/$name"
        
        echo "Downloading: $name"
        curl -s -L -o "$output_path" "$url"
        echo "Saved to: $output_path"
    done
}

# Find and process subdirectories
echo "$CONTENTS" | grep -o '"type":"dir","name":"[^"]*"' | while read -r item; do
    # Extract name
    DIR_NAME=$(echo "$item" | sed 's/.*"name":"\([^"]*\)".*/\1/')
    
    # Process the subdirectory
    process_directory "$PATH_IN_REPO/$DIR_NAME" "$OUTPUT_DIR/$DIR_NAME"
done

echo "-------------------------------------------"
echo "Download completed!" 