import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile
import sqlite3
import os

# Create data directory if it doesn't exist
data_dir = './data'
os.makedirs(data_dir, exist_ok=True)

# Function to download Excel file from a ZIP archive and convert it to a DataFrame
def download_and_convert_to_csv(url):
    """Download Excel file from a ZIP archive and convert it to a DataFrame."""
    print(f"Downloading data from {url}...")
    response = requests.get(url)
    with ZipFile(BytesIO(response.content)) as myzip:
        with myzip.open(myzip.namelist()[0]) as myfile:
            df = pd.read_excel(myfile, engine='openpyxl')
            print(f"Columns in the {url.split('/')[-1]} dataset:", df.columns.tolist())  # Show actual columns
    return df

# Function to preprocess data (select relevant columns, rename, and clean)
def preprocess_data(job_df, food_df):
    """Preprocess data by selecting relevant columns, renaming them, and cleaning data."""

    # Select and rename columns in the job dataset
    job_df = job_df[['DUID', 'JOBTYPE', 'HRSPRWK', 'GROSSPAY', 'DAYWAGE', 'OFFTAKEI']].rename(columns={
        'DUID': 'dwelling_unit_id',
        'JOBTYPE': 'job_type',
        'HRSPRWK': 'hours_per_week',
        'GROSSPAY': 'gross_pay',
        'DAYWAGE': 'daily_wage',
        'OFFTAKEI': 'offered_insurance_accepted'
    })

    # Select and rename columns in the food dataset
    food_df = food_df[['DUID', 'FSOUT42', 'FSLAST42', 'FSAFRD42', 'FSSKIP42', 'FSWT42']].rename(columns={
        'DUID': 'dwelling_unit_id',
        'FSOUT42': 'food_out_worry',
        'FSLAST42': 'food_not_last',
        'FSAFRD42': 'could_not_afford_meal',
        'FSSKIP42': 'meal_skip',
        'FSWT42': 'food_weight'
    })

    # Convert relevant columns to numeric and remove invalid (non-numeric) values
    numeric_columns_job = ['hours_per_week', 'gross_pay', 'daily_wage', 'offered_insurance_accepted']
    numeric_columns_food = ['food_out_worry', 'food_not_last', 'could_not_afford_meal', 'meal_skip', 'food_weight']

    for column in numeric_columns_job:
        job_df[column] = pd.to_numeric(job_df[column], errors='coerce')

    for column in numeric_columns_food:
        food_df[column] = pd.to_numeric(food_df[column], errors='coerce')

    # Drop rows with any remaining NaN values
    job_df = job_df.dropna()
    food_df = food_df.dropna()

    # Merge datasets on 'dwelling_unit_id' (Dwelling Unit ID)
    merged_df = job_df.merge(food_df, on='dwelling_unit_id', how='inner')

    return merged_df

# Main execution function
def main():
    # URLs to the ZIP files containing the data
    job_url = 'https://meps.ahrq.gov/mepsweb/data_files/pufs/h237/h237xlsx.zip'
    food_security_url = 'https://meps.ahrq.gov/mepsweb/data_files/pufs/h240/h240xlsx.zip'

    # Download and process the datasets
    job_df = download_and_convert_to_csv(job_url)
    food_df = download_and_convert_to_csv(food_security_url)

    # Preprocess and merge data
    merged_df = preprocess_data(job_df, food_df)

    # Display the merged DataFrame head and the first 15 rows
    print("Head of the merged DataFrame:")
    print(merged_df.head())

    print("\nDisplaying 15 rows from the merged DataFrame:")
    print(merged_df.head(15))

    # Ensure the /data directory exists
    data_directory = './data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # Create an SQLite database connection
    db_path = os.path.join(data_directory, 'merged_dataset.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Store the merged DataFrame in the SQLite database
    merged_df.to_sql('merged_data', conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()

    # Query the first 5 rows from the merged data table
    query = "SELECT * FROM merged_data LIMIT 5"
    queried_df = pd.read_sql_query(query, conn)

    # Display the first 5 rows of the queried DataFrame to confirm
    print("\nQueried DataFrame from SQLite (first 5 rows):")
    print(queried_df)

    # Close the connection
    conn.close()

    # Save the merged DataFrame to a CSV file in the /data directory
    output_csv = os.path.join(data_directory, 'merged_dataset.csv')
    merged_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\nMerged dataset saved as {output_csv}")

# Execute the script
if __name__ == '__main__':
    main()
