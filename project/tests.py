import unittest
import os
import subprocess
import sqlite3
import pandas as pd

# Paths to validate
DB_FILE = './data/merged_dataset.db'
CSV_FILE = './data/merged_dataset.csv'
PIPELINE_FILE = 'pipeline.py'

class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run the pipeline script before tests."""
        print("Running pipeline.py...")
        pipeline_path = os.path.abspath("pipeline.py")  # Absolute path to pipeline.py

        # Explicitly use Python executable
        result = subprocess.run(
            ["python", pipeline_path],
            capture_output=True,
            text=True
        )

        # Check for errors during pipeline execution
        if result.returncode != 0:
            print("Error running pipeline.py")
            print(result.stderr)
            raise RuntimeError("Pipeline execution failed")
        print("pipeline.py executed successfully.")

    def test_csv_file_exists(self):
        """Test if the CSV output file exists."""
        print("Checking if CSV file exists...")
        self.assertTrue(os.path.exists(CSV_FILE), f"CSV file not found: {CSV_FILE}")
        print("CSV file exists.")

    def test_database_file_exists(self):
        """Test if the SQLite database file exists."""
        print("Checking if SQLite database file exists...")
        self.assertTrue(os.path.exists(DB_FILE), f"Database file not found: {DB_FILE}")
        print("SQLite database file exists.")

    def test_csv_file_content(self):
        """Test if the CSV file contains data."""
        print("Validating CSV file content...")
        df = pd.read_csv(CSV_FILE)
        self.assertFalse(df.empty, "CSV file is empty.")
        print(f"CSV file contains {len(df)} rows.")

    def test_database_table(self):
        """Test if the SQLite database contains the 'merged_data' table."""
        print("Validating SQLite database structure...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if 'merged_data' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='merged_data';")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table, "Table 'merged_data' not found in the database.")
        print("'merged_data' table exists in the database.")

    def test_database_content(self):
        """Test if the 'merged_data' table contains rows."""
        print("Checking if 'merged_data' table has rows...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM merged_data;")
        row_count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(row_count, 0, "'merged_data' table is empty.")
        print(f"'merged_data' table contains {row_count} rows.")


# Run the tests
if __name__ == '__main__':
    unittest.main()
    print("All tests passed.")

