import sys
import bitmap_convert
import pythonenv

def download_images(characters=None):
    import requests
    import os
    import json
    
    # Load the currentResponse.json file
    try:
        with open('./currentResponse.json', 'r') as file:
            data = json.load(file)
        
        # Check if the JSON has the expected structure
        if 'toys' not in data:
            print("Warning: currentResponse.json does not contain 'toys' field")
            return
        
        characters_data = data['toys']
        
        for index, character in enumerate(characters_data):
            # Check if character has a bmpUrl
            if 'bmpUrl' not in character:
                print(f"Warning: Toy at index {index} does not have a bmpUrl")
                continue
            
            bmp_url = character['bmpUrl']
            
            # Check if a file matching the current index exists in the specified directory
            index_file_path = f"./displaycode/pic/toy-img/{character['key']}.bmp"
            if not os.path.isfile(index_file_path):
                try:
                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(index_file_path), exist_ok=True)
                    
                    # Download the file
                    print(f"Downloading {bmp_url} to {index_file_path}")
                    response = requests.get(bmp_url)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    
                    # Save the file
                    with open(index_file_path, 'wb') as file:
                        file.write(response.content)
                    
                    print(f"Successfully downloaded and saved {index_file_path}")
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading {bmp_url}: {e}")
                except IOError as e:
                    print(f"Error saving file to {index_file_path}: {e}")
            else:
                print(f"File {index_file_path} already exists, skipping download")
    
    except FileNotFoundError:
        print("Error: currentResponse.json file not found")
    except json.JSONDecodeError:
        print("Error: currentResponse.json is not a valid JSON file")
    except Exception as e:
        print(f"Unexpected error: {e}")

def download_voices(characters):
    return;

def download_json():
    import requests
    import os
    import json
    from datetime import datetime
    import vercel_blob
    
    os.environ["BLOB_READ_WRITE_TOKEN"] = pythonenv.BLOB_READ_WRITE_TOKEN

    # Get the list of blobs from Vercel Blob Storage
    response = vercel_blob.list()
    
    try:
        # Filter blobs to only include those with pathname or url containing "userData"
        userData_files = []
        for blob in response['blobs']:
            if 'userData' in blob['pathname'] or 'userData' in blob['url']:
                userData_files.append(blob)
        
        if not userData_files:
            print("No userData files found in the Vercel Blob Storage.")
            return None
        
        # Sort files by uploadedAt timestamp (most recent first)
        userData_files.sort(key=lambda x: x['uploadedAt'], reverse=True)
        
        # Get the latest file
        latest_file = userData_files[0]
        file_url = latest_file['url']
        
        print(f"Found latest userData file: {file_url} (uploaded at {latest_file['uploadedAt']})")
        
        # Download the latest file
        response = requests.get(file_url)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs("./", exist_ok=True)
        
        # Save the file
        local_path = f"./currentResponse.json"
        with open(local_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Successfully downloaded and saved latest userData file to {local_path}")
        
        # Parse and return the JSON data
        try:
            json_data = json.loads(response.content)
            return json_data
        except json.JSONDecodeError:
            print("Warning: Downloaded file is not valid JSON")
            return None
            
    except Exception as e:
        print(f"Error downloading userData file: {e}")
        return None

def convert_images_to_bmps(characters):
    for index, character in enumerate(characters):
        image_path = f"./displaycode/pic/toy-img/{character['key']}.bmp"
        bmp_path = f"./displaycode/pic/toy-bmp/{character['key']}.bmp"
        print(f"Converting {image_path} to {bmp_path}")
        bitmap_convert.place_image_in_square(image_path, bmp_path, 120)
