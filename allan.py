import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_allan_deviation(data, Fs):
    """
    Calculate the Allan deviation for a given dataset and sampling frequency.
    
    Parameters:
    - data: numpy array of data
    - Fs: Sampling frequency
    
    Returns:
    - tau: Array of time intervals
    - adev: Array of Allan deviation values
    """
    # Define sample period
    t0 = 1 / Fs

    # Calculate the angle theta
    theta = np.cumsum(data) * t0
    L = len(theta)

    # Define the range for m and tau
    max_m = 2 ** np.floor(np.log2(L / 2)) 
    m = np.logspace(np.log10(10), np.log10(max_m), num=100) # Create log-spaced array
    m = np.ceil(m).astype(int) # Convert to integer
    m = np.unique(m)  # Remove duplicates

    tau = m * t0

    # Initialize Allan variance array
    avar = np.zeros(len(m))

    # Calculate Allan variance
    for i, mi in enumerate(m):
        two_mi = 2 * mi
        avar[i] = np.sum((theta[1+two_mi:L] - 2 * theta[1+mi:L-mi] + theta[1:L-two_mi])**2)

    avar /= (2 * tau**2 * (L - 2 * m))

    # Calculate Allan deviation
    adev = np.sqrt(avar)

    return tau, adev

def plot_allan_deviation(tau, adev):
    """Plot the Allan deviation."""
    plt.figure(figsize=(10, 6))
    plt.loglog(tau, adev)
    plt.grid()
    plt.gca().set_aspect('equal')
    plt.xlabel('Tau (s)')
    plt.ylabel('Allan deviation')
    plt.title('Allan Deviation Plot')
    plt.show()

# Example usage
file_path = 'output2.csv'
Fs = 100
data_field='MagData1'

df = pd.read_csv(file_path)
data = df[data_field].to_numpy()
tau, adev = calculate_allan_deviation(data, Fs)
plot_allan_deviation(tau, adev)
