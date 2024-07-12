## Generic CSV Data Plotting Script

This script provides a versatile tool to visualize data from multiple columns in a CSV file. It offers customization options for labels, colors, and the x-axis.

### Requirements

* **Python:** Ensure you have Python installed on your system. You can check by running `python --version` or `python3 --version` in your terminal. If not installed, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **Libraries:** Make sure you have the `pandas` and `matplotlib` libraries installed in your Python environment. You can install them using pip:

```bash
pip install pandas matplotlib
```

2. **Replace placeholders:**
   - Update `filename` with the path to your CSV file containing the data.
   - Modify `columns_to_plot` with the list of column names you want to visualize (e.g., `["ColData1", "ColData2", "ColData3"]`).
   - Optionally, provide custom labels for each column in the `labels` list (same order as `columns_to_plot`). If not provided, column names will be used as labels.
   - Optionally, specify the column name for the x-axis in `x_axis_to_use` (default uses DataFrame index).
3. **Run the script:**
   - Execute the script using `python plotter.py` (replace with your actual script filename).

### Function Description

The script defines a function named `plot_data` that accepts the following arguments:

- `filename`: Path to the CSV file (string).
- `columns`: List of column names to be plotted (list of strings).
- `labels` (optional): List of labels for each plot (list of strings, defaults to column names).
- `colors` (optional): List of colors for each plot (list of strings, defaults to ['blue', 'green', 'red', 'black']).
- `figsize` (optional): Size of the figure as a tuple (width, height) in inches (defaults to (15, 10)).
- `x_axis` (optional): Name of the column to be used as the x-axis (string, defaults to DataFrame index).

The function performs the following steps:

  - Reads the CSV data using `pandas`.
  - Creates a figure with subplots for each column.
  - Plots the data from each column with labels, colors, grids, and legends.

### Example Usage

```python
# Replace with your data file path
filename = "your_data.csv"

# Columns to plot (assuming data in these columns)
columns_to_plot = ["ColData1", "ColData2", "ColData3"]

# Optional custom labels
labels = ["Custom Label 1", "Custom Label 2", "Custom Label 3"]

# Optional x-axis column name (if not using index)
x_axis_to_use = "TimeColumn"  

# Call the function to generate the plot
plot_data(filename, columns_to_plot, labels=labels, x_axis=x_axis_to_use)
