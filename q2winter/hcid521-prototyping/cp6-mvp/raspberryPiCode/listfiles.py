import os

def list_files_recursive(folder_path, output_file="file_list.txt"):
    """
    Recursively lists files in a folder and its subdirectories, saving them to a text file.
    Filenames are saved in the format "/[folder-name]/[filename]".

    Args:
        folder_path (str): The path to the root folder.
        output_file (str): The name of the output text file. Defaults to "file_list.txt".
    """
    try:
        with open(output_file, "w") as f:
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    relative_path = os.path.relpath(os.path.join(root, filename), folder_path)
                    if os.path.sep != "/": #convert windows paths to unix style
                        relative_path = relative_path.replace(os.path.sep, "/")

                    f.write("/" + relative_path + "\n")

        print(f"File list (including subdirectories) saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
folder_path = "./"  # Replace with the actual folder path
list_files_recursive(folder_path)
