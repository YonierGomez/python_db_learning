import pymysql

DROP_TABLE_USER = "DROP TABLE IF EXISTS user"

USER_TABLE = """CREATE TABLE IF NOT EXISTS user (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""

if __name__ == '__main__':
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='neytor', 
                            passwd='neytor', db='neytor-db')
        
        #PARA EJECUTAR SENTENCIAS SQL NOS APOYAMOS DE UN CURSOR
        cursor = conn.cursor()  
        
        #YA CON EL OBJETO CURSOR PODEMOS EJECUTAR LAS SENTENCIAS SQL
        cursor.execute(DROP_TABLE_USER)
        cursor.execute(USER_TABLE)
        print('Connection successful')
        
    except pymysql.MySQLError as e:
        print('Error: ', e)
        
        
    finally:
        conn.close()
        print('Connection closed')
        cursor.close()  
        print('Cursor closed')