import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
file_path = "output2.csv"
data_field = "MagData1"
Fs = 100

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

def plot_allan_deviation(adev, tau):
    """Plot the Allan deviation."""
    plt.figure(figsize=(10, 6))
    plt.loglog(tau, adev)
    plt.grid()
    plt.gca().set_aspect('equal')
    plt.xlabel('Tau (s)')
    plt.ylabel('Allan deviation')
    plt.title('Allan Deviation Plot')
    plt.show()

def find_angle_random_walk(adev, tau,slope = -0.5):
    """
    This function finds the angle random walk coefficient (N) from Allan deviation data.

    Args:
        adev (numpy.ndarray): Array of Allan deviation values.
        tau (numpy.ndarray): Array of time constants (tau).
        slope (float, optional): Target slope for slope estimation (defaults to 0.5).

    Returns:
        float: The angle random walk coefficient (N).
    """

    # Calculate logarithmic values
    logtau = np.log10(tau)
    logadev = np.log10(adev)

    # Calculate finite difference for slope estimation
    dlogadev = np.diff(logadev) / np.diff(logtau)

    # Find index of closest slope value in the finite difference
    i = np.argmin(np.abs(dlogadev - slope))

    # Calculate y-intercept (b) and logN
    b = logadev[i]-slope*logtau[i]
    logN = slope * np.log(1) + b

    # Calculate N (angle random walk coefficient)
    N = 10**logN

    # Plot parameters
    tauN = 1  # Reference tau for N calculation
    lineN = N / np.sqrt(tau)

    return N, tauN, lineN

def find_rate_random_walk(adev, tau, slope=0.5):
  """
  This function finds the rate random walk coefficient (K) from Allan deviation data.

  Args:
      tau (numpy.ndarray): Array of time constants.
      adev (numpy.ndarray): Array of Allan deviation values.
      slope (float, optional): Target slope for slope estimation (defaults to 0.5).

  Returns:
      float: The rate random walk coefficient (K).
  """

  # Calculate logarithmic values
  logtau = np.log10(tau)
  logadev = np.log10(adev)

  # Calculate finite difference for slope estimation
  dlogadev = np.diff(logadev) / np.diff(logtau)

  # Find index of closest slope value in the finite difference
  i = np.argmin(np.abs(dlogadev - slope))

  # Calculate y-intercept (b) and logK
  b = logadev[i] - slope * logtau[i]
  logK = slope * np.log10(3) + b

  # Calculate K (rate random walk coefficient)
  K = 10**logK

  # Plot parameters
  tauK = 3
  lineK = K * np.sqrt(tau/3) # RRW contribution

  return K, tauK, lineK

def find_bias_instability(tau, adev, slope=0):
  """
  This function finds the bias instability coefficient (B) from Allan deviation data.

  Args:
      tau (numpy.ndarray): Array of time constants.
      adev (numpy.ndarray): Array of Allan deviation values.
      slope (float, optional): Target slope for slope estimation (defaults to 0).

  Returns:
      float: The bias instability coefficient (B).
  """

  # Calculate logarithmic values
  logtau = np.log10(tau)
  logadev = np.log10(adev)

  # Calculate finite difference for slope estimation
  dlogadev = np.diff(logadev) / np.diff(logtau)

  # Find index of closest slope value in the finite difference
  i = np.argmin(np.abs(dlogadev - slope))

  # Calculate y-intercept (b)
  b = logadev[i] - slope * logtau[i]

  # Scaling factor for bias instability calculation
  scfB = np.sqrt(2 * np.log(2) / np.pi)

  # Calculate logB and bias instability coefficient (B)
  logB = b - np.log10(scfB)
  B = 10**logB

  # Plot parameters
  tauB = tau[i]
  lineB = B * scfB * np.ones_like(tau)

  return B, tauB, lineB, scfB


def plot_allan_deviation_arw(tau, adev, N, title="Allan Deviation with Angle Random Walk",
                             xlabel=r'$\tau$', ylabel=r'$\sigma(\tau)$', legend_labels=(r'$\sigma$', r'$\sigma_N$')):
  """
  Plots the Allan deviation data with the noise contribution line from angle random walk.

  Args:
      tau (numpy.ndarray): Array of time constants.
      adev (numpy.ndarray): Array of Allan deviation values.
      N (float): Angle random walk coefficient.
      title (str, optional): Title for the plot. Defaults to "Allan Deviation with Angle Random Walk".
      xlabel (str, optional): Label for the x-axis. Defaults to "\\tau" (LaTeX for tau).
      ylabel (str, optional): Label for the y-axis. Defaults to "\\sigma(\\tau)" (LaTeX for sigma(tau)).
      legend_labels (tuple, optional): Labels for the legend entries. Defaults to ("\\sigma", "\\sigma_N").
  """

  # Calculate the noise contribution line
  tauN = 1  # Reference tau for N calculation
  lineN = N / np.sqrt(tau)

  # Create the plot
  plt.figure()
  plt.loglog(tau, adev, label=legend_labels[0])  # Use legend_labels for sigma
  plt.loglog(tau, lineN, '--', label=legend_labels[1])  # Use legend_labels for sigma_N
  plt.loglog(tauN, N, 'o',label='N')

  # Set plot labels and title
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  # Add legend and text annotation
  plt.legend()

  # Enable grid and set equal aspect ratio
  plt.grid(True)
  plt.gca().set_aspect('equal')

  # Display the plot
  plt.show()

import matplotlib.pyplot as plt
import numpy as np

def plot_allan_deviation_noise(tau, adev, noise_coeffs={}, 
                          title="Allan Deviation with Noise Parameters", xlabel=r'$\tau$', ylabel=r'$\sigma(\tau)$',
                          legend_labels={'ADEV':r'$\sigma$', 'ARW':r'$\sigma_N$', 'RRW':r'$\sigma_K$', 'BI':r'$\sigma_B$'}):
  """
  This function plots Allan deviation data with contributions from different noise sources.

  Args:
      tau (numpy.ndarray): Array of time constants.
      adev (numpy.ndarray): Array of Allan deviation values.
      noise_coeffs (dict, optional): Dictionary containing noise coefficients and reference taus.
          Keys are 'N' (angle random walk), 'K' (rate random walk), or 'B' (bias instability).
          Values are tuples containing (coefficient, reference tau, noise contribution line).
      title (str, optional): Title for the plot. Defaults to "Allan Deviation with Noise Parameters".
      xlabel (str, optional): Label for the x-axis. Defaults to "\\tau" (LaTeX for tau).
      ylabel (str, optional): Label for the y-axis. Defaults to "\\sigma(\\tau)" (LaTeX for sigma(tau)).
      legend_labels (tuple, optional): Labels for the legend entries.
  """

  if not noise_coeffs:
     title = "Allan Deviation Plot"

  # Calculate noise contribution lines and marker points
  lines = []
  points = []
  for noise_type, noise_data in noise_coeffs.items():
      if noise_type == 'B':
        coeff, tau_ref, line, scfB = noise_data
      else:
        coeff, tau_ref, line = noise_data  
      if noise_type == 'N':
          lines.append((tau, line, 'ARW', '--'))
          points.append((tau_ref, coeff, 'N', 'o', 'red'))
      elif noise_type == 'K':
          lines.append((tau, line, 'RRW', '-.'))
          points.append((tau_ref, coeff, 'K', 'o', 'green'))
      elif noise_type == 'B':
        #   scfB = noise_data[3]  # Scaling factor for BI
          lines.append((tau, line, 'BI', ':'))
          points.append((tau_ref, coeff * scfB , 'B', 'o', 'blue'))
      else:
          raise ValueError(f"Invalid noise type: {noise_type}. Supported types are 'N', 'K', and 'B'.")

  # Create the plot
  plt.figure(figsize=(12,8))
  plt.loglog(tau, adev, label=legend_labels['ADEV'])
  for tau_i, line_i, label_i, style_i in lines:
      plt.loglog(tau_i, line_i, style_i, label=legend_labels[label_i])

  for tau_i, line_i, label_i, style_i, color_i in points:
      plt.loglog(tau_i, line_i, style_i, color=color_i)
      plt.text(tau_i, line_i, f'{label_i}={line_i:.2e}', fontsize=12)

  # Set plot labels and title
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  # Add legend (if labels provided)
  if legend_labels:
      plt.legend(loc='upper right')

  # Enable grid and set equal aspect ratio
  plt.grid(True)
  plt.gca().set_aspect('equal')

  # Display the plot
  plt.show()

if __name__ == '__main__':
    # Read data from CSV
    df = pd.read_csv(file_path)

    # Extract data from the specified field
    data = df[data_field].to_numpy()

    # Calculate Allan deviation
    tau, adev = calculate_allan_deviation(data, Fs)

    # Plot the Allan deviation
    # plot_allan_deviation(tau, adev)

    # Find the angle random walk coefficient
    N,tauN,lineN = find_angle_random_walk(adev, tau)
    print(f"Angle Random Walk Coefficient (N): {N}")
    # Plot the Allan deviation with angle random walk
    # plot_allan_deviation_arw(tau, adev, N)

    # Find the rate random walk coefficient
    K,tauK,lineK = find_rate_random_walk(adev, tau)
    print(f"Rate Random Walk Coefficient (K): {K}")

    # Find the bias instability coefficient
    B,tauB,lineB,scfB = find_bias_instability(tau, adev)
    print(f"Bias Instability Coefficient (B): {B}")

    # Plot the Allan deviation with noise parameters
    noise_coeffs = {'N': (N,tauN,lineN), 'K': (K,tauK,lineK), 'B': (B,tauB,lineB,scfB)}
    plot_allan_deviation_noise(tau, adev, noise_coeffs)


