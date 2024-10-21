import pymysql
# Importamos la libreria decouple para leer las variables de entorno
from decouple import config

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
        conn = pymysql.connect(host='127.0.0.1', 
                                port=3306, 
                                user=config('DB_USER'), 
                                passwd=config('DB_PASS'), 
                                db=config('DB_NAME') 
                                )
        
        #PARA EJECUTAR SENTENCIAS SQL NOS APOYAMOS DE UN CURSOR
        with conn.cursor() as cursor:
            #YA CON EL OBJETO CURSOR PODEMOS EJECUTAR LAS SENTENCIAS SQL
            cursor.execute(DROP_TABLE_USER)
            cursor.execute(USER_TABLE)
            
            #INSERTAR UN REGISTRO
            username = 'Manuel'
            password = 'passwordManuel'
            email = 'manuel@aprendiendo.com'
            
            query = f"INSERT INTO user (username, password, email) VALUES ('{username}', '{password}', '{email}')"
            # Ejecutamos la consulta
            cursor.execute(query)
            
            
            # Guardamos los cambios en la base de datos
            conn.commit()
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')