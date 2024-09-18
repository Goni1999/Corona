# Function to read file as bytes
def read_file_as_bytes(file_path):
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

# Function to convert bytes to a hexadecimal string
def bytes_to_hex_string(byte_content):
    return " ".join(f"{byte:02x}" for byte in byte_content)

# Function to save the hexadecimal string to a text file
def save_hex_string_to_file(hex_string, output_path):
    try:
        with open(output_path, "w") as file:
            file.write(hex_string)
        print(f"Hex string saved to '{output_path}'.")
    except IOError as e:
        print(f"Error writing file: {e}")

# Main function to convert a Python file to a hexadecimal representation
def convert_python_file_to_hex(file_path, output_path):
    byte_content = read_file_as_bytes(file_path)
    if byte_content is not None:
        hex_string = bytes_to_hex_string(byte_content)
        save_hex_string_to_file(hex_string, output_path)
    else:
        print("Conversion failed.")

# Usage
file_path = "kizagan_client_building.py"  # Replace with the path to your Python file
output_path = "output_file.txt"  # Replace with your desired output text file path
convert_python_file_to_hex(file_path, output_path)
