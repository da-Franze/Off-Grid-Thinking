from PIL import Image
import numpy as np
import zlib
import sys

def encode_to_images(input_data, image_size=(512, 512)):
    """
    Encodes binary data into multiple images with True-Color (24-bit) support and zlib compression.
    """
    width, height = image_size
    total_pixels = width * height
    capacity_per_image = total_pixels * 3  # 3 bytes per pixel (RGB)
    max_chunk_size = capacity_per_image - 8  # Subtract 8 bytes for the header

    # Compress data
    compressed_data = zlib.compress(input_data)
    total_data_length = len(compressed_data)
    print(f"Compressed data length: {total_data_length} bytes")

    # Split data into chunks for multiple images
    images = []
    num_images = (total_data_length + max_chunk_size - 1) // max_chunk_size  # Calculate number of images
    print(f"Total images required: {num_images}")

    for i in range(num_images):
        start = i * max_chunk_size
        end = min(start + max_chunk_size, total_data_length)
        chunk = compressed_data[start:end]

        # Add header for order and length
        chunk_length = len(chunk).to_bytes(4, 'big')
        header = i.to_bytes(2, 'big') + num_images.to_bytes(2, 'big') + chunk_length
        padded_data = header + chunk
        padded_data = padded_data.ljust(capacity_per_image, b'\x00')  # Pad to full image size

        # Convert to image
        pixel_data = np.frombuffer(padded_data, dtype=np.uint8).reshape((height, width, 3))
        image = Image.fromarray(pixel_data, mode='RGB')
        images.append(image)

    return images


def decode_from_images(images):
    """
    Decodes binary data from multiple images with True-Color (24-bit) support and zlib decompression.
    """
    compressed_data = b""  # Initialize as bytes, not string
    for img in images:
        # Convert image to raw data
        pixel_data = np.array(img, dtype=np.uint8).flatten()

        # Extract header
        chunk_index = int.from_bytes(pixel_data[:2], 'big')
        total_images = int.from_bytes(pixel_data[2:4], 'big')
        chunk_length = int.from_bytes(pixel_data[4:8], 'big')

        # Extract data chunk
        chunk = bytes(pixel_data[8:8 + chunk_length].tolist())  # Convert to bytes
        compressed_data += chunk  # Concatenate bytes

    # Decompress data
    return zlib.decompress(compressed_data)


def save_images(images, output_prefix):
    """
    Saves a list of images with the given prefix.
    """
    for i, img in enumerate(images):
        img.save(f"{output_prefix}_{i + 1}.png")
    print(f"Saved {len(images)} images as '{output_prefix}_*.png'.")


def load_images(input_prefix, num_images):
    """
    Loads a list of images with the given prefix.
    """
    images = []
    for i in range(1, num_images + 1):
        img = Image.open(f"{input_prefix}_{i}.png")
        images.append(img)
    print(f"Loaded {num_images} images from '{input_prefix}_*.png'.")
    return images


if __name__ == "__main__":
    print("Script started...")
    if len(sys.argv) < 3:
        print("Usage: python 3D_Multi_Bilddaten.py <input-file> <output-prefix> [--decode=<num-images>]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_prefix = sys.argv[2]

    if len(sys.argv) == 4 and sys.argv[3].startswith("--decode="):
        # Decode mode
        num_images = int(sys.argv[3].split('=')[1])
        try:
            images = load_images(input_file, num_images)
            decoded_data = decode_from_images(images)
            output_file = f"{output_prefix}_decoded"
            with open(output_file, "wb") as f:
                f.write(decoded_data)
            print(f"Data successfully decoded into '{output_file}'.")
        except Exception as e:
            print(f"An error occurred during decoding: {e}")
    else:
        # Encode mode
        try:
            with open(input_file, "rb") as f:
                input_data = f.read()

            images = encode_to_images(input_data, image_size=(512, 512))  # Use 512x512 size
            save_images(images, output_prefix)
        except Exception as e:
            print(f"An error occurred during encoding: {e}")
