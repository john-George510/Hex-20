# Allan Deviation Calculation and Noise Analysis

This script calculates the Allan deviation for a given dataset and analyzes different noise parameters, including Angle Random Walk (ARW), Rate Random Walk (RRW), and Bias Instability (BI). The results are visualized using a log-log plot.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Function Descriptions](#function-descriptions)
- [Usage](#usage)
- [Configuration File](#configuration-file)
- [Example](#example)

## Requirements

Ensure you have the following requirements met before running the script:

- **Python:** Make sure Python is installed on your system. Verify by running `python --version` or `python3 --version` in your terminal. If Python is not installed, download it from [python.org](https://www.python.org/downloads/).

- **Libraries:** The script requires `numpy`, `pandas`, `matplotlib`, and `json`. Install them using pip:

    ```bash
    pip install numpy pandas matplotlib
    ```

## Configuration File

Create a `config.json` file with the following structure:

```json
{
  "filePath": "path/to/your/data.csv",
  "dataField": "name_of_the_data_column"
}
```

## Setup

1. **Prepare the CSV file:** Ensure your CSV file is formatted correctly and accessible. The file should contain the data you wish to analyze.

2. **Create a configuration file:** Create a `config.json` file to specify the data file path and the data field name.

3. **Run the script:** Execute the script using:

    ```bash
    python allan_dev.py
    ```

## Function Descriptions

The script includes several functions for calculating Allan deviation and noise parameters, as well as plotting the results.

### `calculate_allan_deviation`

Calculates the Allan deviation for a given dataset and sampling frequency.


### `find_angle_random_walk`

Finds the angle random walk coefficient (N) from Allan deviation data.


### `find_rate_random_walk`

Finds the rate random walk coefficient (K) from Allan deviation data.


### `find_bias_instability`

Finds the bias instability coefficient (B) from Allan deviation data.


### `plot_allan_deviation_noise`

Plots Allan deviation data with contributions from different noise sources.


