import sqlite3
# this is custom package will be present in learning respository
# from python_learned.Sqlite import SqliteDefs 
from utils.SQLITE import SqliteDefs

if __name__ == '__main__':

    db_path = 'data\exercise_database.sqlite'
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()
    # ➖➖➖➖➖➖➖➖➖➖➖➖ ACTIONS PEFORMED ON SCRAPED DATABASE ➖➖➖➖➖➖➖➖➖➖➖➖
    # SqliteDefs.create_new_table_from_a_column_of_existing_table(cursor,'Execise','muscle',"Muscles",'muscle')
    # SqliteDefs.add_foreign_key(cursor,'Exercise','muscle_id','Muscles','muscle_id')
    # SqliteDefs.populate_foreign_keys_based_on_condition(cursor,'Exercise','muscle_id',
    #                                                     'Muscles','muscle_id',
    #                                                     'Exercise.muscle = Muscles.muscle')
    # ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # Commit the changes and close the cursor and the connection
    conn.commit()
    cursor.close()
    conn.close()
