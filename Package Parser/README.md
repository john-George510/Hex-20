# Packet Parser

This project contains a packet parser that reads a binary file containing data packets, parses the packets based on a specified format, and writes the parsed data to a CSV file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

To use this packet parser, you need to have Python installed along with the following packages:

- `struct`
- `pandas`
- `json`
- `tqdm`

You can install the required packages using the following command:

```bash
pip install pandas tqdm
```

## Usage

1. Prepare a configuration file named `config.json` with the following structure:

    ```json
    {
        "packetFormat": "path/to/format/file",
        "dataPacket": "path/to/binary/file"
    }
    ```

2. Ensure that your format file defines the structure of your data packets. It should contain lines that specify the fields within the packets. Each line should follow this format:

    ```
    APPEND <field_name> <field_size> <field_type> <field_length>
    ```

    For example:

    ```
    APPEND field1 1 UINT 1
    APPEND field2 2 UINT 2
    APPEND_ARRAY_ITEM field3 4 FLOAT 16
    ```

3. Run the script:

    ```bash
    python parser.py
    ```

    The script will:
    - Read the format file and binary data file specified in the configuration file.
    - Parse the packets based on the format.
    - Write the parsed data to a CSV file with the same name as the binary file but with a `.csv` extension.

4. The CSV file will be created in the same directory as the binary file, containing the parsed packet data.

