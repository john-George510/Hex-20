import matplotlib.pyplot as plt
import pandas as pd

# Function to plot generic data from a CSV
def plot_data(filename, columns, labels=None, colors=['blue', 'green', 'red', 'black'], figsize=(15, 10), x_axis=None):
  """
  Plots data from specified columns in a CSV file.

  Args:
      filename (str): Path to the CSV file.
      columns (list): List of column names to be plotted.
      labels (list, optional): List of labels for each plot (optional). Defaults to None.
      colors (list, optional): List of colors for each plot (optional). Defaults to ['blue', 'green', 'red', 'black'].
      figsize (tuple, optional): Size of the figure (optional). Defaults to (15, 10).
      x_axis (str, optional): Name of the column to be used as the x-axis (optional). Defaults to index.

  Example Usage:
      Replace with your actual file path and desired columns:

      filename = "your_data.csv"
      columns_to_plot = ["column1", "column2", ...]
      x_axis_to_use = "SensorTime"  # Optional, specify x-axis column name

      plot_data(filename, columns_to_plot, x_axis=x_axis_to_use)

  """

  # Read data from CSV
  df = pd.read_csv(filename)

  # Create the figure
  plt.figure(figsize=figsize)

  # Check if labels are provided, otherwise use column names
  if labels is None:
      labels = columns

  # If x_axis is not specified, use DataFrame's index as x-axis data
  # Otherwise, use the specified column in DataFrame as x-axis data
  x_data = df.index if x_axis is None else df[x_axis]

  # Loop through each column and plot
  for i, col in enumerate(columns):
      plt.subplot(len(columns), 1, i + 1)  # Adjust based on number of columns
      plt.plot(x_data, df[col], label=labels[i], color=colors[i % len(colors)])
      plt.xlabel(x_axis if x_axis else 'index')  # Use the specified x-axis label
      plt.ylabel(col)
      plt.title(f'{col} vs {x_axis}')
      plt.legend()

  # Adjust layout and display the plot
  plt.tight_layout()
  plt.show()


# Replace with your actual file path and desired columns
filename = "ads_data.csv"
columns_to_plot = ["MagData1","MagData2","MagData3"]

plot_data(filename, columns_to_plot)
