#!/usr/bin/env python3
import os
import requests
import base64
from urllib.parse import urlparse

def download_github_folder(github_url, local_dir='.'):
    """
    Download all files from a GitHub repository folder
    
    Args:
        github_url (str): URL to the GitHub folder
        local_dir (str): Local directory to save files to
    """
    # Parse the GitHub URL to extract owner, repo, and path
    parsed_url = urlparse(github_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) < 5 or path_parts[2] != 'tree':
        print(f"Invalid GitHub URL format: {github_url}")
        return False
    
    owner = path_parts[0]
    repo = path_parts[1]
    branch = path_parts[3]
    path = '/'.join(path_parts[4:])
    
    # GitHub API URL to get contents of the folder
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    
    print(f"Downloading files from: {github_url}")
    print(f"API URL: {api_url}")
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        contents = response.json()
        
        # Create the target directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Download each file in the folder
        for item in contents:
            if item['type'] == 'file':
                file_url = item['download_url']
                file_path = os.path.join(local_dir, item['name'])
                
                print(f"Downloading: {item['name']}")
                
                # Download the file
                file_response = requests.get(file_url)
                file_response.raise_for_status()
                
                # Save the file
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
                
                print(f"Saved to: {file_path}")
            elif item['type'] == 'dir':
                # Recursively download subdirectories
                subdir_url = f"https://github.com/{owner}/{repo}/tree/{branch}/{path}/{item['name']}"
                subdir_path = os.path.join(local_dir, item['name'])
                download_github_folder(subdir_url, subdir_path)
        
        print(f"Download completed successfully!")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading files: {e}")
        return False

if __name__ == "__main__":
    # URL to the GitHub folder
    github_url = "https://github.com/kwokm/mhcid2025-coursework/tree/main/q2winter/hcid521-prototyping/cp6-mvp/raspberry-pi-code"
    
    # Local directory to save files to (current directory by default)
    local_dir = "."
    
    # Download the files
    download_github_folder(github_url, local_dir)