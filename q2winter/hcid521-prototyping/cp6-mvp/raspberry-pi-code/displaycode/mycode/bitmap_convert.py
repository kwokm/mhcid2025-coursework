from PIL import Image
import argparse

def place_image_in_square(input_path, output_path, square_size):
    """Places an image inside a square canvas, maintaining aspect ratio, and saves as BMP."""
    original_image = Image.open(input_path).convert('L')
    original_width, original_height = original_image.size

    aspect_ratio = original_width / original_height

    if original_width > original_height:
        new_width = square_size
        new_height = int(square_size / aspect_ratio)
    else:
        new_height = square_size
        new_width = int(square_size * aspect_ratio)

    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    square_canvas = Image.new('L', (square_size, square_size), 0)

    x_offset = (square_size - new_width) // 2
    y_offset = (square_size - new_height) // 2

    square_canvas.paste(resized_image, (x_offset, y_offset))

    square_canvas = square_canvas.point(lambda x: 0 if x < 128 else 255, '1')

    # Save as BMP
    square_canvas.save(output_path, "bmp")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert an image to a square bitmap while maintaining aspect ratio.')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('output_path', help='Path for the output BMP file')
    parser.add_argument('--size', type=int, default=120, help='Size of the square canvas (default: 120)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    place_image_in_square(args.input_file, args.output_path, args.size)
    print(f"Converted {args.input_file} to {args.output_path} with square size {args.size}")

if __name__ == "__main__":
    main()