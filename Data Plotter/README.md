# Generic CSV Data Plotting Script

This script provides a versatile tool to visualize data from multiple columns in a CSV file. It offers customization options for labels, colors, and the x-axis.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Configuration File](#configuration-file)
- [Function Description](#function-description)

## Requirements

Ensure you have the following requirements met before running the script:

- **Python:** Make sure Python is installed on your system. Verify by running `python --version` or `python3 --version` in your terminal. If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

- **Libraries:** The script requires `pandas` and `matplotlib`. Install them using pip:

    ```bash
    pip install pandas matplotlib
    ```

## Setup

1. **Prepare the CSV file:** Ensure your CSV file is formatted correctly and accessible. The file should contain the data you wish to plot.

2. **Create a configuration file:** Create a `config.json` file to specify the data file path, columns to plot, labels, and the x-axis column name.

3. **Run the script:**
   - Execute the script using:

    ```bash
    python plotter.py
    ```

## Configuration File

Create a `config.json` file with the following structure:

The x_axis_column_name field is optional. If it is not specified in the JSON, the index of the data will be used as the x-axis.

If the output_file field is not specified in the JSON, the input filename (data.csv) will be used as the default output image name.
```json
{
  "filename": "path/to/your/data.csv",
  "columns_to_plot": ["ColData1", "ColData2", "ColData3"],
  "labels": ["Custom Label 1", "Custom Label 2", "Custom Label 3"],
  "x_axis_column_name": "TimeColumn",
  "output_file":"output.png"
}
```

## Function Description

The script includes a function named `plot_data`, which is responsible for reading the CSV file and generating the plots.

### `plot_data` Function

The `plot_data` function accepts the following parameters:

- **filename** (str): Path to the CSV file.
- **columns** (list of str): List of column names to be plotted.
- **labels** (list of str, optional): Custom labels for each plot. Defaults to column names.
- **colors** (list of str, optional): Colors for each plot. Defaults to `['blue', 'green', 'red', 'black']`.
- **figsize** (tuple, optional): Size of the figure in inches (width, height). Defaults to `(15, 10)`.
- **x_axis** (str, optional): Column name to use for the x-axis. Defaults to DataFrame index.

### Steps Performed

1. Reads the CSV data using `pandas`.
2. Creates a figure with subplots for each column specified.
3. Plots the data from each column with the specified labels and colors.
4. Adds grid lines and legends to the plots.
