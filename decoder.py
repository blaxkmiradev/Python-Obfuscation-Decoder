import base64
import zlib
import re
import os

def decode_layer(content):
    match = re.search(r"b'(.+?)'\)\)$", content, re.DOTALL)
    if not match:
        match = re.search(r"b'(.+?)'\)$", content, re.DOTALL)
    if match:
        encoded = match.group(1)
        return zlib.decompress(base64.b64decode(encoded[::-1]), 15).decode('utf-8')
    return None

def main():
    file_path = input("Enter file path to decode: ").strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    layers = 0
    while True:
        decoded = decode_layer(content)
        if decoded is None:
            break
        content = decoded
        layers += 1
        print(f"Decoded layer {layers} (size: {len(content)} bytes)")

    if layers == 0:
        print("No encoded layers found.")
        return

    output_path = os.path.splitext(file_path)[0] + "_decoded.py"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nDone! {layers} layers decoded.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
