import unittest
import os
import pandas as pd
import sqlite3
from pipeline import main  

class TestDataPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run the main function to execute the data pipeline."""
        main()

    def test_csv_file_exists(self):
        """Test if the CSV output file exists."""
        self.assertTrue(
            os.path.isfile('./data/merged_dataset.csv'),
            "CSV output file does not exist."
        )

    def test_sqlite_file_exists(self):
        """Test if the SQLite database file exists."""
        self.assertTrue(
            os.path.isfile('./data/merged_dataset.db'),
            "SQLite database file does not exist."
        )

    def test_csv_file_content(self):
        """Test if the CSV file has data."""
        csv_path = './data/merged_dataset.csv'
        df = pd.read_csv(csv_path)
        self.assertFalse(df.empty, "CSV file is empty.")
        self.assertGreater(len(df), 0, "CSV file has no data rows.")

    def test_sqlite_file_content(self):
        """Test if the SQLite database table has data."""
        db_path = './data/merged_dataset.db'
        conn = sqlite3.connect(db_path)
        query = "SELECT COUNT(*) FROM merged_data"
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0, "SQLite database table 'merged_data' is empty.")

    def test_merged_columns(self):
        """Test if the merged dataset contains expected columns."""
        csv_path = './data/merged_dataset.csv'
        df = pd.read_csv(csv_path)
        expected_columns = [
            "dwelling_unit_id",
            "job_type",
            "hours_per_week",
            "gross_pay",
            "daily_wage",
            "offered_insurance_accepted",
            "food_out_worry",
            "food_not_last",
            "could_not_afford_meal",
            "meal_skip",
            "food_weight"
        ]
        self.assertTrue(
            all(column in df.columns for column in expected_columns),
            "Merged dataset does not contain the expected columns."
        )

if __name__ == '__main__':
    unittest.main()
