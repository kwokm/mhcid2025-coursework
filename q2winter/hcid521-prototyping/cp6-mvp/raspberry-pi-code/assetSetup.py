import sys

sys.path.append('./displaycode/mycode')
import bitmap_convert

def download_bmps(characters):
    import requests
    import os
    
    for index, character in enumerate(characters):
        # Check if a file matching the current index exists in the specified directory
        index_file_path = f"/displaycode/mycode/toy-bmps/{index}.bmp"
        if not os.path.isfile(index_file_path):
            print(f"Downloading BMP for {character['name']}")
            bmp_url = f"https://toys-to-stories-web.vercel.app/toy-photos/bmp/{index}.bmp"
            
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(index_file_path), exist_ok=True)
                
                # Download the file
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

def download_voices(characters):
    return;

def convert_images_to_bmps(characters):
    for index, character in enumerate(characters):
        image_path = f"/displaycode/pic/toy-photos/{index}.jpg"
        bmp_path = f"/displaycode/pic/toy-bmps/{index}.bmp"
        bitmap_convert.place_image_in_square(image_path, bmp_path, 120)
