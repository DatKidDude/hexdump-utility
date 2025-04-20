import argparse
from dataclasses import dataclass
import os

@dataclass
class Row:
    offset: int
    hex_str: str
    ascii_str: str


def format_chunk(chunk: bytes) -> str:
    """Reverses byte ordering and returns it as hexadecimal"""
    return chunk[::-1].hex()


def valid_cols(value):
    """Verify the column range is between 0 and 255"""
    ivalue = int(value)
    if ivalue < 0 or ivalue > 255:
        raise argparse.ArgumentTypeError("cols must be between 0 and 255")

    return ivalue

def hexdump(source, little_endian, group, length, cols, seek_offset):
    # Array to hold the Row object
    rows = []

    # If cols is 0 set it to the default value
    cols = 16 if cols == 0 else cols

    with open(source, "rb") as file:
        file.seek(seek_offset)
        binary_data = file.read(length)
        
        # Add binary data to Row dataclass
        for row in range(0, len(binary_data), cols):
            # Store the offset
            offset = row
            # Grab 16 bytes at a time
            hex_data = binary_data[row: row + cols]
            if little_endian:
                # Reverse the byte groups 
                hex_pairs = [format_chunk(hex_data[i:i + group]) for i in range(0, len(hex_data), group)]
                hex_str = " ".join(hex_pairs)
            else:
                # Group the hexdump output by `group` size bytes
                # As long as you slice bytes it stays a byte object 
                hex_str = " ".join([hex_data[i: i + group].hex() for i in range(0, len(hex_data), group)])
            # Create the ASCII text 
            ascii_str = "".join([chr(i) if 32 <= i <= 126 else "." for i in hex_data])
            # Store the Row objects in an array
            rows.append(Row(offset, hex_str, ascii_str))

    # Format for the hexdump output
    for r in rows:
        print(f"{r.offset:08X}: {r.hex_str} {r.ascii_str}")

def main():
    parser = argparse.ArgumentParser(
        prog="ccxxd",
        description="ccxxd creates a hex dump of a given file"
    )

    parser.add_argument("file", help="File to parse")
    parser.add_argument("-e", "--endian", action="store_true", help="Little endian byte ordering")
    parser.add_argument("-g", "--group", type=int, default=2, choices=[1,2,4,8], help="Separate the output of every <bytes> bytes (two hex characters or eight bit-digits each) by a whitespace. Defaults to 2")
    parser.add_argument("-l", "--length", type=int, help="Stop after writing <length> octets.")
    parser.add_argument("-c", "--cols", type=valid_cols, default=16, help="format <cols> octets per line. Default 16")
    parser.add_argument("-s", "--seek", type=int, default=0, help="Start at <seek> bytes in the file.")

    args = parser.parse_args()

    # Read up to length bytes 
    if args.length:
        hexdump(args.file, args.endian, args.group, args.length, args.cols, args.seek)
    else:
        # Read the whole file if length is not provided
        file_size = os.path.getsize(args.file)
        hexdump(args.file, args.endian, args.group, file_size, args.cols, args.seek)

if __name__ == "__main__":
    main()

# -s 96 files.tar