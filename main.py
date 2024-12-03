import pandas as pd

def filter_baltimore_addresses(input_file, output_file, zip_codes, st_types):
    try:
        # Load the CSV file
        data = pd.read_csv(input_file)
        
        # Debugging: Print column names and first few rows
        print("Columns in the CSV file:")
        print(data.columns)
        print("First few rows of the dataset:")
        print(data.head())
        
        # Clean and standardize the ZIP_CODE column
        data['ST_TYPE'] = data['ST_TYPE'].astype(str).str.strip()  # Standardize street types
        data['ZIP_CODE'] = data['ZIP_CODE'].astype(str).str.strip()  # Standardize ZIP codes
        data['ZIP_CODE'] = data['ZIP_CODE'].str[:5]  # Extract first 5 characters of ZIP codes
        data = data[data['ZIP_CODE'].str.isdigit()]  # Retain rows where ZIP_CODE is numeric
        data['ZIP_CODE'] = data['ZIP_CODE'].astype(int)  # Convert ZIP_CODE to integers

        # Filter rows by ZIP codes and street types
        filtered_data = data[
            (data['ZIP_CODE'].isin(zip_codes)) & (data['ST_TYPE'].isin(st_types))
        ]
        
        # Debugging: Check if data is being filtered
        print(f"Number of rows matching ZIP codes and street types: {len(filtered_data)}")

        # Make a copy of filtered_data to avoid "SettingWithCopyWarning"
        filtered_data = filtered_data.copy()

        # Clean and standardize BLDG_NO
        filtered_data['BLDG_NO'] = filtered_data['BLDG_NO'].apply(
            lambda x: str(int(float(x))) if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else ''
        )

        # Replace 'AVE' with 'AV' in ST_TYPE column
        filtered_data['ST_TYPE'] = filtered_data['ST_TYPE'].replace("AVE", "AV")

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
        21275, 21278, 21279, 21281, 21287, 21289, 21290, 21297, 21298, 0
    ]

    # List of valid street types
    st_types = [
        "AL", "AVE", "BLVD", "CIR", "CT", "DR", "GRTH", "HWY",
        "LA", "MALL", "MEWS", "PASS", "PATH", "PIKE", "PKWY",
        "PL", "PLZA", "RD", "SQ", "ST", "TR", "WAKL", "WAY"
    ]

    # Run the filtering function
    filter_baltimore_addresses(input_file, output_file, baltimore_zip_codes, st_types)
