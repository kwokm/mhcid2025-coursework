import os
import re

def rename_files_replace_spaces_and_numbers(folder_path, replace_char="-", remove_numbers=True):
    """
    Recursively scans a folder and its subdirectories.
    Renames all files by replacing spaces with the specified character and optionally removing numbers.
    Ensures no filename conflicts occur during renaming.

    Args:
        folder_path (str): The path to the root folder.
        replace_char (str): Character to replace spaces with. Defaults to "-".
        remove_numbers (bool): Whether to remove numbers from filenames. Defaults to True.
    """
    renamed_count = 0
    skipped_count = 0
    
    try:
        # First collect all paths to avoid modification during iteration
        all_files = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if " " in filename or (remove_numbers and any(c.isdigit() for c in filename)):
                    file_path = os.path.join(root, filename)
                    all_files.append(file_path)
        
        # For conflict detection, get all existing files grouped by directory
        existing_files_by_dir = {}
        for root, _, files in os.walk(folder_path):
            existing_files_by_dir[root] = set(files)
        
        # Now process the collected files
        for file_path in all_files:
            dir_path, filename = os.path.split(file_path)
            name, ext = os.path.splitext(filename)
            
            # Create new filename with spaces replaced
            new_name = name.replace(" ", replace_char)
            
            # Remove numbers if requested
            if remove_numbers:
                new_name = re.sub(r'\d+', '', new_name)
                
            # Clean up potential double separators and leading/trailing separators
            new_name = re.sub(f'{replace_char}+', replace_char, new_name)
            new_name = new_name.strip(replace_char)
            
            # Make sure we have a non-empty filename
            if not new_name:
                new_name = "file"  # Default name if everything was removed
            
            new_filename = new_name + ext
            
            # Skip if the filename didn't change
            if new_filename == filename:
                continue
                
            # Check for conflicts
            conflict = False
            if new_filename in existing_files_by_dir[dir_path] and new_filename != filename:
                # There's already a file with the new name
                conflict = True
                
                # Try to resolve by adding an index
                index = 1
                while conflict and index < 100:  # Limit to avoid infinite loop
                    indexed_name = f"{new_name}_{index}{ext}"
                    if indexed_name not in existing_files_by_dir[dir_path] or indexed_name == filename:
                        new_filename = indexed_name
                        conflict = False
                    index += 1
            
            if conflict:
                print(f"Skipped: '{filename}' (Conflict with existing files)")
                skipped_count += 1
                continue
                
            new_file_path = os.path.join(dir_path, new_filename)
            
            # Update our record of existing files for this directory
            existing_files_by_dir[dir_path].add(new_filename)
            if filename in existing_files_by_dir[dir_path]:
                existing_files_by_dir[dir_path].remove(filename)
            
            # Rename the file
            try:
                os.rename(file_path, new_file_path)
                renamed_count += 1
                print(f"Renamed: '{filename}' → '{new_filename}'")
            except Exception as e:
                print(f"Error renaming {file_path}: {e}")
                skipped_count += 1
        
        print(f"\nProcessing complete!")
        print(f"Renamed {renamed_count} files")
        print(f"Skipped {skipped_count} files due to conflicts or errors")
        
        if remove_numbers:
            print(f"- Replaced spaces with '{replace_char}' and removed numbers")
        else:
            print(f"- Replaced spaces with '{replace_char}'")
                    
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Rename files by replacing spaces and optionally removing numbers")
    parser.add_argument("folder_path", nargs="?", default=".", help="Path to the folder containing files to rename")
    parser.add_argument("--replace-char", "-r", default="-", help="Character to replace spaces with (default: '-')")
    parser.add_argument("--keep-numbers", "-k", action="store_true", help="Keep numbers in filenames (default: remove numbers)")
    
    args = parser.parse_args()
    
    rename_files_replace_spaces_and_numbers(
        args.folder_path, 
        replace_char=args.replace_char,
        remove_numbers=not args.keep_numbers
    ) 