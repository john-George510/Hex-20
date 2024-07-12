import struct
import pandas as pd
import json
from tqdm import tqdm

def read_and_parse_format_file(file_path):
  """
  Reads and parses the format file to construct a list of dictionaries,
  where each dictionary contains details about a specific field in the packet.

  Args:
      file_path (str): Path to the format file containing packet structure definitions.

  Returns:
      list: A list of dictionaries, each representing a packet field with details
          like name, format string, size, data type, and length.
  """

  packet_format = []

  # Open the format file and read all lines
  with open(file_path, 'r') as file:
    format_data = file.readlines()

  # Process each line in the format file
  for line in format_data:
    # Skip comment lines that start with '#'
    if line.startswith('#'):
      continue

    # Split the line into parts based on whitespace
    parts = line.split(' ')

    # Check if the line starts with 'APPEND' indicating a field definition
    if parts[0].startswith('APPEND'):
      # Extract field details from the line
      packet_field = parts[1]  # Name of the field in the packet
      field_size = int(parts[2])  # Size of a single data element in bytes
      field_type = parts[3]  # Data type of the field (e.g., UINT, FLOAT)
      field_length = int(parts[4]) if parts[0] == 'APPEND_ARRAY_ITEM' else field_size  # Total length of the field in bytes
      field_count = field_length // field_size  # Number of data elements in the field (if applicable)

      # Determine the format string based on field type and size for unpacking data later
      type_char = ''
      if field_type == 'UINT':
        type_char = {8: 'B', 16: 'H', 32: 'L'}.get(field_size, '')  # Map size to format string for unsigned integers
      elif field_type == 'FLOAT' and field_size == 32:
        type_char = 'f'  # Format string for single-precision floats

      if type_char:
        field_format = f"<{field_count}{type_char}"  # Construct the format string

        # Create a dictionary containing details about the parsed field
        field_info = {
            'name': packet_field,
            'format': field_format,
            'size': field_size,
            'data_type': field_type,
            'length': field_length
        }

        # Append the field information dictionary to the packet_format list
        packet_format.append(field_info)

  return packet_format

def parse_and_write_packets(data, header_bytes, packet_format, output_file):
  """
  Parses packets from binary data and writes them directly to a CSV file.

  Args:
      data (bytes): Binary data containing the packets to be parsed.
      header_bytes (bytes): Byte sequence that marks the beginning of a packet.
      packet_format (list): List of dictionaries containing details about
          each field within the packets, including name, format string, size,
          data type, and length.
      output_file (str): Path to the output CSV file where parsed packets will be written.
  """

  packet_count = 0
  index = 0
  columns_written = False

  # Progress bar for tracking processing
  with tqdm(total=len(data), desc="Processing packets", unit="byte") as pbar:
    prev_index = 0
    while index < len(data):
      # Check for header bytes indicating the start of a packet
      if data[index:index + 3] == header_bytes:
        packet = {}
        packet_index = index + 3

        # Extract packet length from the first byte after the header (assuming this format)
        packet_length = struct.unpack('<B', data[packet_index:packet_index + 1])[0]

        # Check for next header at expected position to avoid incomplete packets
        if data[index + packet_length:index + packet_length + 3] != header_bytes:
          index += 1
          pbar.update(index - prev_index)  # Update progress bar with difference
          prev_index = index
          continue

        # Parse each field within the packet based on the provided format details
        for field in packet_format:
          field_name = field['name']
          field_length = int(field['length'])
          field_format = field['format']

          # Calculate the size of the field data based on the format string
          byte_size = struct.calcsize(field_format)

          # Unpack the field data from the binary data using the format string
          data_value = struct.unpack(field_format, data[packet_index:packet_index + byte_size])

          if field_length == 1:
            # Assign the first element of data_value (single value)
            packet[field_name] = data_value[0]
          else:
            # Handle cases where the field contains multiple values
            for data_index, value in enumerate(data_value):
              packet[f'{field_name}{data_index + 1}'] = value

          # Move the packet index to the start of the next field
          packet_index += byte_size

        # Convert packet data (dictionary) to a DataFrame for easier CSV handling
        packet_df = pd.DataFrame([packet])

        # Write the DataFrame to the CSV file (append mode)
        if not columns_written:
          # Write header row if columns haven't been written yet
          packet_df.to_csv(output_file, mode='a', index=False)
          columns_written = True
        else:
          # Append data rows without header if columns are already written
          packet_df.to_csv(output_file, mode='a', header=False, index=False)

        packet_count += 1
        index = packet_index  # Move to the end of the current packet
        pbar.update(index - prev_index)  # Update progress bar with difference
        pbar.set_postfix_str(f"Processed {packet_count} packets")
        prev_index = index
      else:
        # Update progress bar even if no packet is found
        pbar.update(index - prev_index)
        prev_index = index
        index += 1  # Move to the next byte

  print(f"Processed {packet_count} packets and wrote to {output_file}")

if __name__ == '__main__':

    # Load configuration data from a JSON file
    with open('config.json') as f:
        config = json.load(f)
        
    # Extract paths and parameters from the configuration
    format_file_path = config['packetFormat']
    binary_file_path = config['dataPacket']
    output_file = binary_file_path.replace('.bin', '.csv')
    header_bytes = b'\x48\x32\x30'  # sync_word = H20 in hex

    # Read and parse the format file
    packet_format = read_and_parse_format_file(format_file_path)

    # Read the binary file
    with open(binary_file_path, 'rb') as file:
        data = file.read()

    # Parse packets and write directly to CSV
    parse_and_write_packets(data, header_bytes, packet_format, output_file)
