import sqlite3 

def create_connection(db): 
    connection = None
    try: 
        connection = sqlite3.connect(db)
        return connection 
    except Error as e: 
        print(e)
    return connection 

def create_table(connection, createTblSql): 
    try: 
        cursor = connection.cursor()
        cursor.execute(createTblSql)
    except Error as e: 
        print(e)

def main(): 
    database = 'output/photos.db'

    createTblSql = """ CREATE TABLE IF NOT EXISTS Games (
                                        _id integer PRIMARY KEY,
                                        _photo text NOT NULL,
                                        _x integer NOT NULL,
                                        _y integer NOT NULL,
                                        _difficulty text NOT NULL
                                    ); """
    connection = create_connection(database)

    # create games table
    if connection is not None:
        create_table(connection, createTblSql)
    else:
        print('Connection Error')


if __name__ == '__main__':
    main()