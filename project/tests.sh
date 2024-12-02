#!/bin/bash

# Paths to validate
DB_FILE="./data/merged_dataset.db"
CSV_OUTPUT="./data/merged_dataset.csv"
SCRIPT_NAME="pipeline.py"

# Python executable (updated with your path)
PYTHON_EXEC="/c/Users/Asus/AppData/Local/Programs/Python/Python311/python.exe"

# Check if the Python executable exists
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Error: Python executable not found at $PYTHON_EXEC"
    exit 1
fi

# Run the pipeline
echo "Executing $SCRIPT_NAME..."
$PYTHON_EXEC $SCRIPT_NAME

# Check if the pipeline script executed successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to execute $SCRIPT_NAME"
    exit 1
fi

# Validate the database file existence
echo "Validating output files..."
if [ -f "$DB_FILE" ]; then
    echo "Database file exists: $DB_FILE"
else
    echo "Error: Database file $DB_FILE is missing."
    exit 1
fi

# Validate the CSV file existence
if [ -f "$CSV_OUTPUT" ]; then
    echo "CSV file exists: $CSV_OUTPUT"
else
    echo "Error: CSV file $CSV_OUTPUT is missing."
    exit 1
fi

# Validate database content
echo "Validating database content..."
TABLES=$(sqlite3 "$DB_FILE" ".tables")

# Check if the "merged_data" table exists
if [[ "$TABLES" == *"merged_data"* ]]; then
    echo "Test passed: 'merged_data' table exists in the database."
else
    echo "Error: 'merged_data' table is missing in the database."
    exit 1
fi

# Validate database rows
ROW_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM merged_data;")
if [ "$ROW_COUNT" -gt 0 ]; then
    echo "Test passed: 'merged_data' table contains $ROW_COUNT rows."
else
    echo "Error: 'merged_data' table is empty."
    exit 1
fi

echo "All tests passed successfully."
