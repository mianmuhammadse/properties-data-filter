import pandas as pd

def filter_baltimore_addresses(input_file, output_file, zip_codes):
    try:
        # Load the CSV file
        data = pd.read_csv(input_file)
        
        # Debugging: Print column names and first few rows
        print("Columns in the CSV file:")
        print(data.columns)
        print("First few rows of the dataset:")
        print(data.head())
        
        # Clean and standardize the ZIP_CODE column
        data['ZIP_CODE'] = data['ZIP_CODE'].astype(str).str.strip()  # Remove leading/trailing spaces
        data['ZIP_CODE'] = data['ZIP_CODE'].str[:5]  # Extract the first 5 characters
        data = data[data['ZIP_CODE'].str.isdigit()]  # Keep only rows where ZIP_CODE is numeric
        data['ZIP_CODE'] = data['ZIP_CODE'].astype(int)  # Convert to integers

        # Filter rows by ZIP codes
        filtered_data = data[data['ZIP_CODE'].isin(zip_codes)]
        

        # Debugging: Check if data is being filtered
        print(f"Number of rows matching ZIP codes: {len(filtered_data)}")

        # Clean BLDG_NO to remove '.0'
        filtered_data['BLDG_NO'] = filtered_data['BLDG_NO'].apply(lambda x: str(int(x)) if pd.notnull(x) else '')

        # Extract relevant columns
        addresses = filtered_data[['FULLADDR', 'BLDG_NO', 'STDIRPRE', 'ST_NAME', 'ST_TYPE', 'MAILTOADD', 'ZIP_CODE']]


        # Save to output CSV
        addresses.to_csv(output_file, index=False)
        print(f"Filtered data saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define file paths
    input_file = "Real_Property_Information.csv"
    output_file = "Baltimore_Addresses.csv"

    # List of Baltimore ZIP codes
    baltimore_zip_codes = [
        21201, 21202, 21203, 21205, 21206, 21207, 21208, 21209, 21210, 21211, 21212, 21213,
        21214, 21215, 21216, 21217, 21218, 21222, 21223, 21224, 21225, 21226, 21227, 21229,
        21230, 21231, 21233, 21234, 21236, 21237, 21239, 21251, 21263, 21264, 21270, 21273,
        21275, 21278, 21279, 21281, 21287, 21289, 21290, 21297, 21298
    ]

    # Run the filtering function
    filter_baltimore_addresses(input_file, output_file, baltimore_zip_codes)
