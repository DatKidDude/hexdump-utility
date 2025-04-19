import argparse
from dataclasses import dataclass

@dataclass
class Row:
    offset: int
    hex_str: str
    ascii_str: str


def hexdump(source, group=2):
    # Array to hold the Row object
    rows = []

    with open(source, "rb") as file:
        binary_data = file.read()

        # Each row contains 16 bytes of data
        size = 16
        
        # Add binary data to Row dataclass
        for row in range(0, len(binary_data), size):
            # Store the offset
            offset = row
            # Grab 16 bytes at a time
            hex_data = binary_data[row: row + size]
            # Group the hexdump output by `group` size bytes
            hex_str = " ".join([hex_data[i: i + group].hex() for i in range(0, len(hex_data), group)])
            # Create the ASCII text 
            ascii_str = "".join([chr(i) if 32 <= i <= 126 else "." for i in hex_data])
            # Store the Row objects in an array
            rows.append(Row(offset, hex_str, ascii_str))

    # Format for the hexdump output
    for r in rows:
        print(f"{r.offset:08X}: {r.hex_str} {r.ascii_str}")

def main():

    hexdump("files.tar")
    

if __name__ == "__main__":
    main()