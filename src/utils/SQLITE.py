import sqlite3
class SqliteDefs:
    @staticmethod
    def create_new_table_from_a_column_of_existing_table(cursor, source_table, source_column, dest_table, dest_column):
        """
        Create a new table for distinct values and populate it with unique values from a source table.

        Args:
            cursor (sqlite3.Cursor): The SQLite cursor object connected to the database.
            source_table (str): The name of the source table containing the data.
            source_column (str): The name of the column in the source table to extract unique values from.
            dest_table (str): The name of the destination table to create and populate with unique values.
            dest_column (str): The name of the column in the destination table for storing unique values.

        Returns:
            None

        The function creates a new table for distinct values with a specified name and column name.
        It then inserts unique values from the specified source table and column into the new table.
        If the destination table already exists, it avoids inserting duplicate values.

        Example:
            conn = sqlite3.connect('your_database.db')
            cursor = conn.cursor()

            # Create and populate a Muscles table from the Exercise table
            create_and_populate_table(cursor, 'Exercise', 'muscle', 'Muscles', 'muscle')

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()
        """
        # Create a new table for distinct values
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {dest_table} (
                {dest_column}_id INTEGER PRIMARY KEY NOT NULL,
                {dest_column} TEXT UNIQUE
            )
        ''')

        # Insert distinct values from the source table into the destination table
        cursor.execute(f'''
            INSERT OR IGNORE INTO {dest_table} ({dest_column})
            SELECT DISTINCT {source_column} FROM {source_table}
        ''')

    @staticmethod
    def add_foreign_key(cursor, table_name, new_foreign_key_column, referenced_table, referenced_column):
        """
        Adds a foreign key constraint to a table.
        # NOTE: Constraints not working

        Args:
            cursor (sqlite3.Cursor): The SQLite cursor object.
            table_name (str): The name of the table to which the foreign key will be added.
            new_foreign_key_column (str): The name of the new foreign key column.
            referenced_table (str): The name of the table that is being referenced.
            referenced_column (str): The name of the column in the referenced table.

        Returns:
            None

        Example usage:
        add_foreign_key(cursor, "Orders", "customer_id", "Customers", "customer_id")
        """
        # Step 1: Create a new table with the same columns as the old table, plus the new foreign key column.
        cursor.execute(f'''
            CREATE TABLE {table_name}_new AS
            SELECT *, NULL AS {new_foreign_key_column} FROM {table_name}
        ''')
        # NOTE: CONSTRAINT NOT WORKING IN THE SQLITE
        # Step 2: Add the foreign key constraint to the new table.
        # cursor.execute(f'''
        #     ALTER TABLE {table_name}_new
        #     ADD CONSTRAINT fk_{table_name}_{new_foreign_key_column}
        #     FOREIGN KEY ({new_foreign_key_column}) REFERENCES {referenced_table}({referenced_column})
        # ''')

        # Step 3: Optionally, drop the old table if it's no longer needed.
        cursor.execute(f'DROP TABLE {table_name}')

        # Step 4: Rename the new table to the original table name.
        cursor.execute(f'ALTER TABLE {table_name}_new RENAME TO {table_name}')


    @staticmethod
    def remove_column_from_table(cursor, table_name, column_name):
        """
        Remove a column from a table in an SQLite database.

        Args:
            cursor (sqlite3.Cursor): The SQLite cursor object connected to the database
            table_name (str): The name of the table from which to remove the column.
            column_name (str): The name of the column to be removed.

        Returns:
            None
        """
        try:
            # Connect to the SQLite database
            # Create a new table without the specified column
            cursor.execute(f'''
                CREATE TABLE new_{table_name} AS
                SELECT {', '.join([c[1] for c in cursor.execute(f"PRAGMA table_info({table_name})") if c[1] != column_name])}
                FROM {table_name}
            ''')

            # Delete the old table
            cursor.execute(f'DROP TABLE {table_name}')

            # Rename the new table to the original table name
            cursor.execute(
                f'ALTER TABLE new_{table_name} RENAME TO {table_name}')

            # Commit the changes and close the connection

            print(f"Column '{column_name}' removed from table '{table_name}'.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    # Example usage:
    # remove_column_from_table('your_database.db', 'your_table', 'column_to_be_removed')
    @staticmethod
    def populate_foreign_keys_based_on_condition(cursor, insert_in_table, insert_column, from_table, from_column_values, condition):
        """
        Update records in the destination table with values from a source table based on a condition.

        Args:
            cursor (sqlite3.Cursor): The SQLite database cursor.
            insert_in_table (str): The name of the destination table where records will be updated.
            insert_column (str): The column in the destination table to update with values.
            from_table (str): The name of the source table containing values to be inserted.
            from_column_values (str): The column in the source table containing the values to insert.
            condition (str): The condition to determine which records to update in the destination table.

        Returns:
            None
        """
        cursor.execute(f'''
        UPDATE {insert_in_table}
        SET {insert_column} = (
            SELECT {from_column_values} FROM {from_table} WHERE {condition}
        )
        ''')

    @staticmethod
    def retrieve_data(database_or_cursor, table_name, conditions):
        """
        Retrieve data from an SQLite database based on given conditions.

        Args:
            database_or_cursor (str or sqlite3.Cursor): Either a path to the SQLite
                database file or an existing cursor object.
            table_name (str): The name of the table to query.
            conditions (list): A list of SQL conditions to filter the data.

        Returns:
            list: A list of rows that match the given conditions.

        Example:
            conditions = ["column1 = 'value'", "column2 > 10"]
            data = retrieve_data("mydatabase.db", "mytable", conditions)
        """
        if isinstance(database_or_cursor, str):
            # If a database path is provided, create a new connection and cursor
            connection = sqlite3.connect(database_or_cursor)
            cursor = connection.cursor()
        elif isinstance(database_or_cursor, sqlite3.Cursor):
            # If a cursor is provided, use it directly
            cursor = database_or_cursor
        else:
            raise ValueError("Invalid database_or_cursor argument")

        try:
            # Construct the SQL query with the provided conditions
            query = f"SELECT * FROM {table_name} WHERE {' AND '.join(conditions)}"

            # Execute the query
            cursor.execute(query)

            # Fetch all rows that match the conditions
            rows = cursor.fetchall()

            return rows
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []
        finally:
            if isinstance(database_or_cursor, str):
                # Close the database connection if it was created here
                connection.close()
    @staticmethod
    def retrieve_data_as_dict(database_or_cursor, table_name, conditions):
        """
    Retrieve data from an SQLite database table as a list of dictionaries based on specified conditions.

    Args:
        database_or_cursor: Either a database file path (str) or an existing database cursor (sqlite3.Cursor).
        table_name (str): The name of the table to retrieve data from.
        conditions (list): A list of strings specifying conditions to filter the data (e.g., ["column1 = 'value'", "column2 > 42"]).

    Returns:
        list: A list of dictionaries, where each dictionary represents a row of data. 
              Column names are used as keys, and row values are used as values in the dictionaries.

    Raises:
        ValueError: If an invalid database_or_cursor argument is provided."""
        
        if isinstance(database_or_cursor, str):
            # If a database path is provided, create a new connection and cursor
            connection = sqlite3.connect(database_or_cursor)
            cursor = connection.cursor()
        elif isinstance(database_or_cursor, sqlite3.Cursor):
            # If a cursor is provided, use it directly
            cursor = database_or_cursor
        else:
            raise ValueError("Invalid database_or_cursor argument")

        try:
            # Construct the SQL query with the provided conditions
            query = f"SELECT * FROM {table_name} WHERE {' AND '.join(conditions)}"

            # Execute the query
            cursor.execute(query)

            # Fetch all rows that match the conditions
            rows = cursor.fetchall()
            # Get the column names from the table description
            column_names = [column[0] for column in cursor.description]
            
            # Create a list of dictionaries, where each dictionary represents a row
            data_as_dict = [dict(zip(column_names, row)) for row in rows]


            return data_as_dict
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []
        finally:
            if isinstance(database_or_cursor, str):
                # Close the database connection if it was created here
                connection.close()
            


if __name__ == '__main__':

    # Connect to your SQLite database (replace 'your_database.db' with your database filename)
    conn = sqlite3.connect('c:\Scripts\Learned_Topics\exercise_database.sqlite')
    cursor = conn.cursor()
    # SqliteDefs.add_foreign_key(cursor,'Exercise','muscle_id','Muscles','muscle_id')
    # Update the Exercises table with the associated muscle_id
    cursor.execute('''
        UPDATE Exercise
        SET muscle_id = (
        SELECT muscle_id FROM Muscles WHERE Exercise.muscle = Muscles.muscle
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
