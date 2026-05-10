from PIL import Image
import numpy as np
import zlib
import sys

def encode_to_image(input_data, image_size=(512, 512)):
    """
    Encodes binary data into an image with debugging information.
    """
    width, height = image_size
    total_pixels = width * height

    # Add checksum and original data length
    checksum = zlib.crc32(input_data).to_bytes(4, 'big')
    data_length = len(input_data).to_bytes(4, 'big')  # Store the original data length
    padded_data = checksum + data_length + input_data  # Prefix with checksum and length

    if len(padded_data) > total_pixels:
        raise ValueError("Input data exceeds the capacity of the chosen image size.")
    padded_data = padded_data.ljust(total_pixels, b'\x00')

    # Create pixel data and debug output
    pixel_data = np.frombuffer(padded_data, dtype=np.uint8).reshape((height, width))
    print(f"Raw pixel data (before saving, first 20 bytes): {pixel_data.flatten()[:20].tolist()}")

    # Create and return the image
    image = Image.fromarray(pixel_data, mode='L')
    return image, pixel_data


def decode_from_image(image):
    """
    Decodes binary data from an image with debugging and padding corrections.
    """
    # Convert image to pixel data
    pixel_data = np.array(image, dtype=np.uint8).flatten()
    print(f"Pixel data after loading (first 20 bytes): {pixel_data[:20].tolist()}")

    # Extract checksum and original length
    checksum = bytes(pixel_data[:4])
    original_length = int.from_bytes(pixel_data[4:8], 'big')  # Extract stored length
    extracted_data = bytes(pixel_data[8:8 + original_length])  # Exact slicing based on length

    # Debug: Check the extracted data
    print(f"Extracted raw data length (including padding): {len(pixel_data)} bytes")
    print(f"Extracted data length (expected): {original_length} bytes")
    print(f"Extracted data length (actual): {len(extracted_data)} bytes")
    print(f"Extracted data (first 20 bytes): {extracted_data[:20]}")

    # Verify checksum
    calculated_checksum = zlib.crc32(extracted_data).to_bytes(4, 'big')
    print(f"Extracted checksum: {checksum}")
    print(f"Calculated checksum: {calculated_checksum}")

    if calculated_checksum != checksum:
        raise ValueError("Data integrity check failed: checksum mismatch.")
    if len(extracted_data) != original_length:
        raise ValueError("Extracted data length does not match the original length.")
    return extracted_data


if __name__ == "__main__":
    print("Script started...")  # Debug output on start
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python 3D_Bilddatenübertragung.py <input-file> <output-file> [--decode]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if len(sys.argv) == 4 and sys.argv[3] == "--decode":
        print("Decode mode active...")
        try:
            with Image.open(input_file) as img:
                decoded_data = decode_from_image(img)

            with open(output_file, "wb") as f:
                f.write(decoded_data)

            print(f"Data has been successfully decoded from {input_file} to {output_file}.")
        except Exception as e:
            print(f"An error occurred during decoding: {e}")
    else:
        print("Encode mode active...")
        try:
            with open(input_file, "rb") as f:
                input_data = f.read()

            encoded_image, original_pixel_data = encode_to_image(input_data)
            encoded_image.save(output_file)
            print(f"Data from {input_file} has been successfully encoded into {output_file}.")
        except Exception as e:
            print(f"An error occurred during encoding: {e}")
