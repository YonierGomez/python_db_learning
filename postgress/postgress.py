import psycopg2

DROP_TABLE_USER = "DROP TABLE IF EXISTS users"

USER_TABLE = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

if __name__ == '__main__':
    try:
        connect = psycopg2.connect("dbname='neytor_db' user='neytor' password='neytor' host='127.0.0.1'")
        
        #PARA EJECUTAR SENTENCIAS SQL NOS APOYAMOS DE UN CURSOR
        with connect.cursor() as cursor:
            #YA CON EL OBJETO CURSOR PODEMOS EJECUTAR LAS SENTENCIAS SQL
            cursor.execute(DROP_TABLE_USER)
            cursor.execute(USER_TABLE)
            
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            connect.commit()
                
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM users"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)

            print('='*50)
            print('Eliminamos el ultimo registro')
            print('='*50)
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (4,))
            connect.commit()
            
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM users"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            
    except psycopg2.Error as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        # connect.close()
        print('Connection closed')