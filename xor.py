import sys

KEY = b"\x12\x34\x56"  # Key should be in bytes

def xor(data, key):
    key = key * (len(data) // len(key) + 1)  # Repeat the key to match the length of data
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def print_ciphertext(ciphertext):
    # Convert the ciphertext to hex format and print it
    print('{ 0x' + ', 0x'.join(f"{byte:02X}" for byte in ciphertext) + ' };')

def main():
    if len(sys.argv) != 3:
        print("Usage: python xor.py input_file output_file")
        sys.exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, "rb") as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit()
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit()

    ciphertext = xor(plaintext, KEY)

    try:
        with open(output_file, "w") as f:
            f.write('{ 0x' + ', 0x'.join(f"{byte:02X}" for byte in ciphertext) + ' };')
        print(f"Encoded output saved to {output_file}")
    except IOError as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()
