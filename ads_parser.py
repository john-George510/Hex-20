import struct
import pandas as pd
from tqdm import tqdm

def read_and_parse_format_file(file_path):
    """
    Reads and parses the format file to construct the packet format.

    :param file_path: Path to the format file
    :return: List of dictionaries containing packet format details
    """
    packet_format = []

    # Read the format file line by line
    with open(file_path, 'r') as file:
        format_data = file.readlines()

    # Process each line in the format file
    for line in format_data:
        if line.startswith('#'):  # Skip comment lines
            continue

        parts = line.split(' ')
        if parts[0].startswith('APPEND'):
            # Extract field details from the line
            packet_field = parts[1]
            field_size = int(parts[2])
            field_type = parts[3]
            field_length = int(parts[4]) if parts[0] == 'APPEND_ARRAY_ITEM' else field_size
            field_count = field_length // field_size

            # Determine the format string based on field type and size
            type_char = ''
            if field_type == 'UINT':
                type_char = { 8: 'B', 16: 'H', 32: 'L' }.get(field_size, '')
            elif field_type == 'FLOAT' and field_size == 32:
                type_char = 'f'

            if type_char:
                field_format = f"<{field_count}{type_char}"
                # Append field details to packet_format list
                packet_format.append({
                    'name': packet_field,
                    'format': field_format,
                    'size': field_size,
                    'data_type': field_type,
                    'length': field_length
                })

    return packet_format


def parse_and_write_packets(data, header_bytes, packet_format, output_file):
    """
    Parses packets from binary data and writes them directly to a CSV file.

    :param data: Binary data to parse
    :param header_bytes: Byte sequence indicating the start of a packet
    :param packet_format: List of dictionaries containing packet format details
    :param output_file: Path to the output CSV file
    """
    packet_count = 0
    index = 0
    columns_written = False

    # Initialize tqdm progress bar
    # pbar = tqdm(desc="Processing packets", unit="packet")

    # with tqdm(total=len(data), desc="Processing packets", unit="byte") as pbar:
    
    print("Size of data is: ",len(data))
    with tqdm(total=len(data), desc="Processing packets", unit="byte") as pbar:
        prev_index = 0
        # Process binary data to extract packets
        while index < len(data):
            if data[index:index + 3] == header_bytes:
                packet = {}
                packet_index = index + 3

                # Extract packet length (assuming first byte after header indicates length)
                packet_length = struct.unpack('<B', data[packet_index:packet_index + 1])[0]

                # Check if the next header bytes exist at expected position
                if (data[index + packet_length:index + packet_length + 3] != header_bytes):
                    index += 1
                    pbar.update(index - prev_index)  # Update progress bar with the difference
                    prev_index = index  # Update previous index
                    continue

                # Parse fields in the packet based on packet_format
                for field in packet_format:
                    field_name = field['name']
                    field_length = int(field['length'])
                    field_format = field['format']

                    byte_size = struct.calcsize(field_format)
                    data_value = struct.unpack(field_format, data[packet_index:packet_index + byte_size])

                    if field_length == 1:
                        packet[field_name] = data_value[0]
                    else:
                        for data_index, value in enumerate(data_value):
                            packet[f'{field_name}{data_index + 1}'] = value

                    packet_index += byte_size

                # Convert packet data to DataFrame and write to CSV
                packet_df = pd.DataFrame([packet])

                if not columns_written:
                    packet_df.to_csv(output_file, mode='a', index=False)
                    columns_written = True
                else:
                    packet_df.to_csv(output_file, mode='a', header=False, index=False)

                packet_count += 1
                index = packet_index  # Move to the end of the current packet
                pbar.update(index - prev_index)  # Update progress bar with the difference
                pbar.set_postfix_str(f"Processed {packet_count} packets")
                prev_index = index  # Update previous index
            else:
                pbar.update(index - prev_index)  # Update progress bar with the difference
                prev_index = index  # Update previous index
                index += 1  # Move to the next byte

    # pbar.close()  # Close the progress bar
    print(f"Processed {packet_count} packets and wrote to {output_file}")


if __name__ == '__main__':
    # Paths and parameters
    format_file_path = 'adsfsw_tlm.txt'
    binary_file_path = '2024_07_08_18_14_27_tlm.bin'
    output_file = 'output.csv'
    header_bytes = b'\x48\x32\x30'  # sync_word = H20 in hex

    # Read and parse the format file
    packet_format = read_and_parse_format_file(format_file_path)

    # Read the binary file
    with open(binary_file_path, 'rb') as file:
        data = file.read()

    # Parse packets and write directly to CSV
    parse_and_write_packets(data, header_bytes, packet_format, output_file)
