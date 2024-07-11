import matplotlib.pyplot as plt
import pandas as pd

# Function to plot generic data from a CSV
def plot_data(filename, columns, labels=None,colors = ['blue', 'green', 'red', 'black'], figsize=(15, 10)):
    """
    Plots data from specified columns in a CSV file.

    Args:
        filename (str): Path to the CSV file.
        columns (list): List of column names to be plotted.
        labels (list, optional): List of labels for each plot (optional). Defaults to None.
        figsize (tuple, optional): Size of the figure (optional). Defaults to (10, 6).
    """

    # Read data from CSV
    df = pd.read_csv(filename)

    # Create the figure
    plt.figure(figsize=figsize)

    # Check if labels are provided, otherwise use column names
    if labels is None:
        labels = columns

    # Loop through each column and plot
    for i, col in enumerate(columns):
        plt.subplot(len(columns), 1, i + 1)  # Adjust based on number of columns
        plt.plot(df['time'], df[col], label=labels[i],color=colors[i%len(colors)])
        plt.xlabel('Time')
        plt.ylabel(col)
        plt.title(f'{col} vs Time')
        plt.legend()

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

# Example usage
# Replace with your actual file path and desired columns
filename = "ACS_test.csv"
columns_to_plot = ["Bx", "By", "Bz", "BT"]  # Replace with your desired columns

plot_data(filename, columns_to_plot)
