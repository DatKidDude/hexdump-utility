def main():

    with open("files.tar", "rb") as file:
        binary_data = file.read()

        # Each row contains 16 bytes of data
        size = 16
        # Combine two bytes per row
        step = 2
        
        # Iterate through the file contents
        for row in range(0, len(binary_data), size):
            # Print the row offset in uppercase hexadecimal
            print(f"{row:08X}:", end=" ")
            # Grab 16 bytes at a time
            hex_data = binary_data[row:row + size]
            for i in range(0, len(hex_data), step):
                # Print the hexadecimal values
                print(f"{hex_data[i]:02x}{hex_data[i+1]:02x}", end=" ")
            # Print the ASCII text at the end
            print("".join([chr(i) if 32 <= i <= 126 else "." for i in hex_data]), end="")
            print("")

if __name__ == "__main__":
    main()