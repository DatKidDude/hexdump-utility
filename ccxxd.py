import argparse

def hexdump(source, group=2):
    with open(source, "rb") as file:
        binary_data = file.read()

        # Each row contains 16 bytes of data
        size = 16
        
        # Iterate through the file contents
        for row in range(0, len(binary_data), size):
            # Print the row offset in uppercase hexadecimal
            print(f"{row:08X}:", end=" ")
            # Grab 16 bytes at a time
            hex_data = binary_data[row:row + size]
            print(" ".join([hex_data[i:i + group].hex() for i in range(0, len(hex_data), group)]), end=" ")
            print("".join([chr(i) if 32 <= i <= 126 else "." for i in hex_data]), end="")
            print("")

def main():

    hexdump("files.tar")
    

if __name__ == "__main__":
    main()