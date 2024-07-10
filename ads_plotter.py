import matplotlib.pyplot as plt
import pandas as pd

# Read data from output.csv
df = pd.read_csv('output.csv')

# Calculate mean and standard deviation for each MagData series
mean_mag1 = df['MagData1'].mean()
std_mag1 = df['MagData1'].std()

mean_mag2 = df['MagData2'].mean()
std_mag2 = df['MagData2'].std()

mean_mag3 = df['MagData3'].mean()
std_mag3 = df['MagData3'].std()

# Plot the required columns in subplots
plt.figure(figsize=(15, 10))

# Plot for MagData1 (mag_x)
plt.subplot(3, 1, 1)
plt.plot(df.index, df['MagData1'], label='mag_x', color='blue')
plt.xlabel('Index')
plt.ylabel('Magnitude X')
plt.title('Magnitude X vs Index')
plt.legend()
plt.ylim(mean_mag1 -50, mean_mag1 + 50)  # Set y-axis based on mean and std

# Plot for MagData2 (mag_y)
plt.subplot(3, 1, 2)
plt.plot(df.index, df['MagData2'], label='mag_y', color='green')
plt.xlabel('Index')
plt.ylabel('Magnitude Y')
plt.title('Magnitude Y vs Index')
plt.legend()
plt.ylim(mean_mag2-50, mean_mag2+50)  # Set y-axis based on mean and std

# Plot for MagData3 (mag_z)
plt.subplot(3, 1, 3)
plt.plot(df.index, df['MagData3'], label='mag_z', color='red')
plt.xlabel('Index')
plt.ylabel('Magnitude Z')
plt.title('Magnitude Z vs Index')
plt.legend()
plt.ylim(mean_mag3 - 50, mean_mag3 + 50)  # Set y-axis based on mean and std

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
