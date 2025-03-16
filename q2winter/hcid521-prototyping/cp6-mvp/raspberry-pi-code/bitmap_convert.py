from PIL import Image
import argparse
import os

def place_image_in_square(input_path, output_path, square_size):
    """Places an image inside a square canvas, maintaining aspect ratio, and saves as BMP."""
    # Check if output file already exists
    if os.path.isfile(output_path):
        print(f"Output file {output_path} already exists, skipping conversion")
        return
        
    # Check if input file exists
    if not os.path.isfile(input_path):
        print(f"Input file {input_path} does not exist, cannot convert")
        return
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Open and convert image to grayscale in one step
        original_image = Image.open(input_path).convert('L')
        original_width, original_height = original_image.size

        # Calculate new dimensions while maintaining aspect ratio
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = square_size
            new_height = int(square_size / aspect_ratio)
        else:
            new_height = square_size
            new_width = int(square_size * aspect_ratio)

        # Resize image with LANCZOS resampling (high quality)
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

        # Create a new square canvas
        square_canvas = Image.new('L', (square_size, square_size), 0)

        # Calculate offsets to center the image
        x_offset = (square_size - new_width) // 2
        y_offset = (square_size - new_height) // 2

        # Paste the resized image onto the square canvas
        square_canvas.paste(resized_image, (x_offset, y_offset))

        # Convert to 1-bit (black and white) using a threshold
        square_canvas = square_canvas.point(lambda x: 0 if x < 128 else 255, '1')

        # Save as BMP with optimized settings
        square_canvas.save(output_path, "bmp")
        
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {input_path} to {output_path}: {e}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert an image to a square bitmap while maintaining aspect ratio.')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('output_path', help='Path for the output BMP file')
    parser.add_argument('--size', type=int, default=120, help='Size of the square canvas (default: 120)')
    parser.add_argument('--force', action='store_true', help='Force conversion even if output file exists')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if output file exists and force flag is not set
    if os.path.isfile(args.output_path) and not args.force:
        print(f"Output file {args.output_path} already exists, use --force to overwrite")
        return
    
    # Call the function with the provided arguments
    place_image_in_square(args.input_file, args.output_path, args.size)
    print(f"Converted {args.input_file} to {args.output_path} with square size {args.size}")

if __name__ == "__main__":
    main()