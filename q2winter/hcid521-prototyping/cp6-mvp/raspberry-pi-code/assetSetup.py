import sys
import bitmap_convert
import pythonenv
import os
import json
import requests
import concurrent.futures
import time
from gtts import gTTS

# Global session for better connection pooling
session = requests.Session()

def download_images(characters=None):
    # Load the currentResponse.json file
    try:
        if (characters == None):
            with open('./currentResponse.json', 'r') as file:
                data = json.load(file)
            
            # Check if the JSON has the expected structure
            if 'toys' not in data:
                print("Warning: currentResponse.json does not contain 'toys' field")
                return
            
            characters_data = data['toys']
        else:
            characters_data = characters
        
        # Create directory if it doesn't exist
        os.makedirs("./displaycode/pic/toy-img", exist_ok=True)
        
        # Use ThreadPoolExecutor for parallel downloads
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Create a list to store the futures
            futures = []
            
            for index, character in enumerate(characters_data):
                # Check if character has a bmpUrl
                if 'key' not in character:
                    print(f"Warning: Toy at index {index} does not have a key")
                    continue
                
                bmp_url = f"https://nsqo2pyzsbzn4meq.public.blob.vercel-storage.com/{character['key']}.bmp"
                
                # Check if a file matching the current index exists in the specified directory
                index_file_path = f"./displaycode/pic/toy-img/{character['key']}.bmp"
                if not os.path.isfile(index_file_path):
                    # Submit the download task to the executor
                    future = executor.submit(download_file, bmp_url, index_file_path)
                    futures.append(future)
                else:
                    print(f"File {index_file_path} already exists, skipping download")
            
            # Wait for all downloads to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        print(f"Successfully downloaded and saved {result}")
                except Exception as e:
                    print(f"Error in download task: {e}")
    
    except FileNotFoundError:
        print("Error: currentResponse.json file not found")
    except json.JSONDecodeError:
        print("Error: currentResponse.json is not a valid JSON file")
    except Exception as e:
        print(f"Unexpected error: {e}")

def download_pron(word, lang):
    tts = gTTS(word, lang=lang)
    if lang=="en":
        tts.save(f"./pronounce-audio/{word}.mp3")
    else:
        tts.save(f"./pronounce-translate-audio/{word}-{lang}.mp3")

def download_file(url, file_path):
    """Helper function to download a single file"""
    try:
        # Download the file
        print(f"Downloading {url} to {file_path}")
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save the file
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None
    except IOError as e:
        print(f"Error saving file to {file_path}: {e}")
        return None

def download_pronunciation_audio(characters=None, lang=None):
    # Load the currentResponse.json file
    try:
        if (characters == None):
            with open('./currentResponse.json', 'r') as file:
                data = json.load(file)
            
            # Check if the JSON has the expected structure
            if 'toys' not in data:
                print("Warning: currentResponse.json does not contain 'toys' field")
                return
            
            toys_data = data['toys']
            lang = data['language']
        else:
            toys_data = characters
            lang = lang
        
        # Create directories if they don't exist
        os.makedirs("./pronounce-audio", exist_ok=True)
        os.makedirs("./pronounce-translate-audio", exist_ok=True)
        
        # Collect all download tasks
        download_tasks = []
        
        # Iterate through all toys
        for toy in toys_data:
            # Check if toy has vocab field with nested vocab array
            if 'vocab' not in toy or 'vocab' not in toy['vocab']:
                print(f"Warning: Toy {toy.get('name', 'unknown')} does not have proper vocab structure")
                continue
            
            # Get the vocab array for this toy
            vocab_entries = toy['vocab']['vocab']

            # Process each vocab entry
            for vocab_entry in vocab_entries:
                # Check if vocab entry has a word field
                if 'word' not in vocab_entry:
                    print(f"Warning: Vocab entry in toy {toy.get('name', 'unknown')} does not have a 'word' field")
                    continue
                    
                word = vocab_entry['word']

                # Add pronunciation audio download task
                audio_file_path = f"./pronounce-audio/{word}.mp3"
                
                if not os.path.isfile(audio_file_path):
                    download_tasks.append((word, "en"))
                else:
                    print(f"File {audio_file_path} already exists, skipping download")
                
                translate_audio_file_path = f"./pronounce-translate-audio/{word}-{lang}.mp3"
                    
                if not os.path.isfile(translate_audio_file_path):
                    download_tasks.append((vocab_entry['translation'], lang))
                else:
                    print(f"File {translate_audio_file_path} already exists, skipping download")
        
        # Use ThreadPoolExecutor for parallel downloads
        if download_tasks:
            print(f"Starting parallel download of {len(download_tasks)} audio files...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                # Submit all download tasks
                futures = [executor.submit(download_pron, word, lang) for word, lang in download_tasks]
                
                # Wait for all downloads to complete
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        if result:
                            print(f"Successfully downloaded and saved {result}")
                    except Exception as e:
                        print(f"Error in download task: {e}")
        else:
            print("No audio files need to be downloaded")
    
    except FileNotFoundError:
        print("Error: currentResponse.json file not found")
    except json.JSONDecodeError:
        print("Error: currentResponse.json is not a valid JSON file")
    except Exception as e:
        print(f"Unexpected error: {e}")

def download_voices(characters):
    return;

def download_json():
    import redis
    from datetime import datetime
    
    r = redis.Redis(
    host='happy-kit-31327.upstash.io',
    port=6379,
    password=pythonenv.UPSTASH_REDIS_PASSWORD,
    ssl=True
    )
    
    try:
        # Get the latest userData from Redis
        # Assuming the data is stored with key 'userData'
        json_data = r.get('userData')
        
        if not json_data:
            print("No userData found in Redis")
            return None
            
        # Decode the bytes to string and parse JSON
        try:
            json_data = json.loads(json_data.decode('utf-8'))
            
            # Save to local file for compatibility with existing code
            local_path = "./currentResponse.json"
            os.makedirs("./", exist_ok=True)
            
            with open(local_path, 'w') as file:
                json.dump(json_data, file, indent=2)
            
            print(f"Successfully retrieved and saved userData to {local_path}")
            return json_data
            
        except json.JSONDecodeError:
            print("Warning: Retrieved data is not valid JSON")
            return None
            
    except Exception as e:
        print(f"Error retrieving userData from Redis: {e}")
        return None

def convert_images_to_bmps(characters):
    # Create directory if it doesn't exist
    os.makedirs("./displaycode/pic/toy-bmp", exist_ok=True)
    
    # Use ThreadPoolExecutor for parallel conversion
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Create a list to store the futures
        futures = []
        
        for index, character in enumerate(characters):
            image_path = f"./displaycode/pic/toy-img/{character['key']}.bmp"
            bmp_path = f"./displaycode/pic/toy-bmp/{character['key']}.bmp"
            
            # Skip conversion if output BMP already exists
            if os.path.isfile(bmp_path):
                print(f"BMP file {bmp_path} already exists, skipping conversion")
                continue
                
            # Submit the conversion task to the executor
            future = executor.submit(bitmap_convert.place_image_in_square, image_path, bmp_path, 120)
            futures.append((future, character['key']))
        
        # Wait for all conversions to complete
        for future, key in futures:
            try:
                future.result()
                print(f"Successfully converted image for {key}")
            except Exception as e:
                print(f"Error converting image for {key}: {e}")
