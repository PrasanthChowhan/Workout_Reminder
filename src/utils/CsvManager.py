import os
import csv
import pandas as pd
import sqlite3
from src.utils.constants import DatabaseConstants
from tkinter import filedialog
from pathlib import Path


class CreateCSV:
    def __init__(self, csv_filepath: str = '', dictionary: dict = {}):

        if os.path.exists(csv_filepath):
            append_mode = 'a'  # File exists, open in append mode
        else:
            append_mode = 'w'  # File doesn't exist, open in write mode

        # Extract the header from the keys of the first dictionary
        header = dictionary.keys()

        # Append or create the CSV file and write the data
        with open(csv_filepath, mode=append_mode, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            if append_mode == 'w':
                writer.writeheader()  # Write the header if the file is created
            writer.writerow(dictionary)  # Append dict as row


class CsvAndSQLite:
    # def __init__(self,):

    def csv_to_sqlite(self, csv_filename, db_filename, table_name):
        try:
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(csv_filename)

            # Add a new column 'serial_number' as an integer counter
            df.insert(0, 'exercise_number', range(1, len(df) + 1))

            # Create a SQLite database connection
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()

            # Convert the DataFrame to a SQLite table
            df.to_sql(table_name, conn, index=False, if_exists='replace')

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            print(
                f"✅ CSV file '{csv_filename}' converted to SQLite database '{db_filename}' in table '{table_name}'.")

        except FileNotFoundError:
            print(f"🔴 Error: CSV file '{csv_filename}' not found.")

        except pd.errors.EmptyDataError:
            print(f"🔴 Error: CSV file '{csv_filename}' is empty.")

        except Exception as e:
            print(f"🔴 An unexpected error occurred: {e}")

 # csv structure | name,muscle,difficulty,url
    def create_csv_template(self):
        fieldnames = ["name", "muscle", "difficulty", "url"]
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        # Write CSV file with headers only
        with open(file_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # Write headers
            writer.writeheader()
        print(f"🟢 Empty CSV file with headers created at: {file_path}")

    def add_theme_to_workoutreminder(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        file_name = Path(file_path).stem
        file_name = file_name.replace(" ", "_").strip()

        self.csv_to_sqlite(
            file_path, DatabaseConstants.THEMED_DB_PATH, file_name)


if __name__ == '__main__':
    # file_path = filedialog.askopenfilename( title="Select CSV File",
    #     filetypes=[("CSV files", "*.csv")],)
    CsvAndSQLite.create_csv_template('new.csv')
