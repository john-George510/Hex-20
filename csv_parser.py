import os
import pandas as pd
import json
from datetime import datetime

# Step 1: Load JSON Configuration (Assuming config.json exists)
config_path = "config.json"
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Step 2: Extract Configuration Details
output_folder = config["outputFolder"]
# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

file_details = config["fileDetails"]
folder_root = file_details["folderRoot"]
folder_key = file_details["folderKey"]
folder_path = file_details["folderPath"]
filename = file_details["filename"]

csv_attributes = config["csvAttributes"]
required_columns = csv_attributes["requiredColumns"]

error_folders = []


# Step 3: Loop through folders in the root directory (check only first 5)
for folder in os.listdir(folder_root):
    if os.path.isdir(os.path.join(folder_root, folder)) and folder_key in folder:
        print(f"Processing folder: {folder}")



        # Construct complete file path
        file_path = os.path.join(folder_root, folder, folder_path, filename)

        try:
            # Attempt to read data from the existing CSV
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            error_folders.append({"folder":folder,"error":"file not found"})
            print(f"Error: The file '{file_path}' was not found.")
            continue

        # Create new empty DataFrame for output
        output_df = pd.DataFrame()

        #sort the data by time
        sortParam = csv_attributes["sortBasedOnColumn"]
        df = df.sort_values(by=sortParam, ascending=True)

        print(df.head())

        #convert time to datetime
        
        df['DAXSS Time Stamp (seconds)'] = pd.to_datetime(df['DAXSS Time Stamp (seconds)'], unit='s')

        
        # Get time range for the current DataFrame
        time_range = df[sortParam].min().strftime('%Y_%m_%dT%H_%M_%S') + ' --- ' + df[sortParam].max().strftime('%Y_%m_%dT%H_%M_%S')
        
        print(time_range)
        # Create new CSV filename based on time range
        new_csv_filename = f"{time_range}.csv"
        new_csv_path = os.path.join(output_folder, new_csv_filename)

        print(new_csv_path)

        # Select required columns from existing DataFrame
        csv_columns = df.columns
        for column in required_columns:
            if column in df.columns:
                output_df[column] = df[column]
            else:
                output_df[column] = None

        # Handle missing values (replace with default value)
        output_df = output_df.fillna(csv_attributes["defaultValueForNullValues"])

        print(output_df.head())

        # Save new CSV with formatted filename
        output_df.to_csv(new_csv_path, index=False)
        

print("Error Folders:", error_folders)
print("No of Error Folders:", len(error_folders))