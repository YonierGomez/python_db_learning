## Python DB

Lo consiguiente tiene como objetivo repasar conceptos de python con base de datos.

Lo primero que debemos hacer es generar nuestra base de datos, para esto nos apoyaremos de Docker para tales fines.

## Generar directorio de trabajo

```shell
mkdir -p python_db/mysql_data
```

## Creamos nuestro compose.yaml

```yaml
services:
  mysql:
    image: mysql:latest
    container_name: mysql-container
    environment:
      - MYSQL_ROOT_PASSWORD=neytor # Cambia esto por una contraseña segura
      - MYSQL_DATABASE=neytor-db         # Nombre de la base de datos que se creará al iniciar
      - MYSQL_USER=neytor                    # Usuario que se creará
      - MYSQL_PASSWORD=neytor       # Contraseña del usuario
    ports:
      - "3306:3306"  # Exponer el puerto para acceder a la base de datos
    volumes:
      - $PWD/mysql_data:/var/lib/mysql  # Persistencia de datos
```

## Corremos nuestro compose.yaml

Ejecutamos el siguiente comando en el directorio donde está nuestro compose.yaml

```shell
docker compose -p work_db_python up -d
```

## Crear entorno virtual

```shell
python3 -m venv env
```

## Generar archivos en python

### Conexión

Generamos nuestro archivo **db.py** 

### Instalar modulo pymysql

```shell
pip install pymysql
```

### db.py

```python
import pymysql

if __name__ == '__main__':
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='neytor', 
                            passwd='neytor', db='neytor-db')
    
        print('Connection successful')
        
    except pymysql.MySQLError as e:
        print('Error: ', e)
```

### Explicación

* A través del método connect creamos un objeto tipo conn y pasamos los argumentos de **host, port, user, passwd, db**

## Crear tabla

```python
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
```

### Explicación:

Hacemos uso del método **cursor** que está en el objeto **conn** creado anteriormente, este nos devuelve un objeto tipo cursor el cual tiene un método **execute** el cual nos permite ejecutar sentencias SQL.

## Conexión bajo contexto

Con esto podemos obtener un código pythonico, harémos un re-factor

Para esto utilizamos la sentencia `with` el cual incluso ya cierra la conexión 

```python
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
        with conn.cursor() as cursor:
            #YA CON EL OBJETO CURSOR PODEMOS EJECUTAR LAS SENTENCIAS SQL
            cursor.execute(DROP_TABLE_USER)
            cursor.execute(USER_TABLE)
            print('Connection successful')
        
    except pymysql.MySQLError as e:
        print('Error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

### Explicación

Eliminamos cursor = conn.cursor()  a favor del contexto haciendo uso de with

## Variables de entorno

En nuestro so host definiremos 3 variables de entorno

```shell
export DB_USER=neytor
export DB_PASS=neytor
export DB_NAME=neytor-db
```

Para obtener variables de entorno podemos apoyarnos de la libreria **os** pero no obstante para este ejemplo usaremos **python-decouple** así que procederemos a instalarla

### Instalar decouple

```shell
pip install python-decouple
```

 

```python
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
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

## Insertar registros

```python
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
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            
            # Los placeholders %s se reemplazan por los valores que se pasan en el segundo argumento
            
            values = ('Yonier', 'password1', 'yonier@aprendiendo.com')
            
            # Ejecutamos la consulta
            cursor.execute(query, values)
            
            # Guardamos los cambios en la base de datos
            conn.commit()
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

### Método format

```python
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
            # query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # # Los placeholders %s se reemplazan por los valores que se pasan en el segundo argumento
            # values = ('Yonier', 'password1', 'yonier@aprendiendo.com')
            
            query = "INSERT INTO user (username, password, email) VALUES ('{}', '{}', '{}')".format('Yonier', 'password1', 'yonier@aprendiendo.com')
            # Ejecutamos la consulta
            # cursor.execute(query, values)
            cursor.execute(query)
            
            
            # Guardamos los cambios en la base de datos
            conn.commit()
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

### F string

```python
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
```

### Explicación

Creamos una variable dentro del contexto el cual tiene una sentencia sql. Los placeholders %s se reemplazan por los valores que se pasan en el segundo argumento en este caso es una dupla que está en **values** 

Se realizan ejemplos con método format y f string, de todos se recomiendan los placeholders.

Ejecutamos la sentencia y guardamos con un commit `conn.commit()`

### Ejemplo de salida

```
mysql> desc user;
+------------+--------------+------+-----+-------------------+-------------------+
| Field      | Type         | Null | Key | Default           | Extra             |
+------------+--------------+------+-----+-------------------+-------------------+
| id         | int unsigned | NO   | PRI | NULL              | auto_increment    |
| username   | varchar(50)  | NO   |     | NULL              |                   |
| password   | varchar(50)  | NO   |     | NULL              |                   |
| email      | varchar(50)  | NO   |     | NULL              |                   |
| created_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+--------------+------+-----+-------------------+-------------------+
5 rows in set (0.01 sec)

mysql> select * from user;
+----+----------+-----------+------------------------+---------------------+
| id | username | password  | email                  | created_at          |
+----+----------+-----------+------------------------+---------------------+
|  1 | Yonier   | password1 | yonier@aprendiendo.com | 2024-10-20 23:14:27 |
+----+----------+-----------+------------------------+---------------------+
1 row in set (0.01 sec)
```

### Insertar múltiples registros

Nos apoyaremos de una lista el cual contiene múltiples tuplas

#### Opción 1 con for

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            for user in users:
                cursor.execute(query, user)

            # Guardamos los cambios en la base de datos
            conn.commit()
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

#### Opcion 2 con executemany

Harémos uso del método `executemany`

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            conn.commit()
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

#### Salida

```
mysql> select * from user;
+----+----------+----------------+------------------------+---------------------+
| id | username | password       | email                  | created_at          |
+----+----------+----------------+------------------------+---------------------+
|  1 | Manuel   | passwordManuel | manuel@aprendiendo.com | 2024-10-20 23:51:06 |
|  2 | Yonier   | passwordYonier | yonier@aprendiendo.com | 2024-10-20 23:51:06 |
|  3 | Iris     | passwordIris   | iris@aprendiendo.com   | 2024-10-20 23:51:06 |
|  4 | Gl       | passwordGl     | gl@aprendiendo.com     | 2024-10-20 23:51:06 |
+----+----------+----------------+------------------------+---------------------+
4 rows in set (0.01 sec)
```

## Obtener registros

Puedes obtener el número de registros así;

```python
# Consulta para obtener todos los registros de la tabla user
query = "SELECT * FROM user"
            
# Ejecutamos la consulta que obtiene la cantidad de registros
rows = cursor.execute(query)
print(rows)
```

Para acceder a los values se debe usar el método `fetchall`

```python
print('='*50)
print('Registros obtenidos')
for row in cursor.fetchall():
    print(row)
```

### Ejemplo completo

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            conn.commit()
            
            # Consulta para obtener todos los registros de la tabla user
            query = "SELECT * FROM user"
            
            # Ejecutamos la consulta que obtiene la cantidad de registros
            rows = cursor.execute(query)
            print(rows)
            
            # Obtenemos todos los registros
            # print(cursor.fetchall())
            print('='*50)
            print('Registros obtenidos')
            for row in cursor.fetchall():
                print(row)
                
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            
                
        
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

## Obtener número limitado de registros

Lo puedes hacer directamente desde la consulta o utilizando el método `fetchmany`

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            conn.commit()
            
            # Consulta para obtener todos los registros de la tabla user
            query = "SELECT * FROM user"
            
            # Ejecutamos la consulta que obtiene la cantidad de registros
            rows = cursor.execute(query)
            print(rows)
            
            # Obtenemos todos los registros
            # print(cursor.fetchall())
            print('='*50)
            print('Registros obtenidos')
            for row in cursor.fetchall():
                print(row)
                
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
                
            print('='*50)
            print('Registros 2 obtenidos')
            print('='*50)
            query = "SELECT username, email FROM user WHERE id LIMIT 2"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
                
            print('='*50)
            print('Registros FETCHMANY LIMIT 2')
            print('='*50)
            query = "SELECT * FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchmany(2):
                print(row)
            
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

## Actualizar registro

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            conn.commit()
                
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)

            print('='*50)
            print('Reemplazamos el primer registro')
            print('='*50)
            query = "UPDATE user SET username = %s WHERE id = %s"
            cursor.execute(query, ('Manuelito', 1))
            conn.commit()
            
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

## Eliminar registros

```python
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

users = [
    ('Manuel', 'passwordManuel', 'manuel@aprendiendo.com'),
    ('Yonier', 'passwordYonier', 'yonier@aprendiendo.com'),
    ('Iris', 'passwordIris', 'iris@aprendiendo.com'),
    ('Gl', 'passwordGl', 'gl@aprendiendo.com'),
]

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
            
            query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
            # Ejecutamos la consulta
            # for user in users:
            #     cursor.execute(query, user)
            
            cursor.executemany(query, users)

            # Guardamos los cambios en la base de datos
            conn.commit()
                
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)

            print('='*50)
            print('Eliminamos el ultimo registro')
            print('='*50)
            query = "DELETE FROM user WHERE id = %s"
            cursor.execute(query, (4,))
            conn.commit()
            
            print('='*50)
            print('Registros obtenidos por columna')
            print('='*50)
            query = "SELECT username, email FROM user"
            rows = cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
            
    except pymysql.MySQLError as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        conn.close()
        print('Connection closed')
```

# Postgress DB

Cambiaremos el gestor de base de datos, en este caso postgress

## Compose.yaml

```yaml
services:
  mysql:
    image: mysql:latest
    container_name: mysql-container
    environment:
      - MYSQL_ROOT_PASSWORD=neytor # Cambia esto por una contraseña segura
      - MYSQL_DATABASE=neytor_db         # Nombre de la base de datos que se creará al iniciar
      - MYSQL_USER=neytor                    # Usuario que se creará
      - MYSQL_PASSWORD=neytor       # Contraseña del usuario
    ports:
      - "3306:3306"  # Exponer el puerto para acceder a la base de datos
    volumes:
      - $PWD/mysql_data:/var/lib/mysql  # Persistencia de datos
      
  postgres:
    image: postgres:latest
    container_name: postgres-container
    environment:
      - POSTGRES_DB=neytor_db           # Nombre de la base de datos que se creará al iniciar
      - POSTGRES_USER=neytor            # Usuario que se creará
      - POSTGRES_PASSWORD=neytor        # Contraseña del usuario
    ports:
      - "5432:5432"  # Exponer el puerto para acceder a la base de datos
    volumes:
      - $PWD/postgres_data:/var/lib/postgresql/data  # Persistencia de datos
```

## Corremos nuestro compose.yaml

Ejecutamos el siguiente comando en el directorio donde está nuestro compose.yaml

```shell
docker compose -p work_db_python up -d

podman-compose -p work_db_python ps
```

## Descargar módulo

```shell
pip install --upgrade pip
pip install psycopg2-binary
```

Si tienes MacOS

```shell
brew install postgresql
pip install --upgrade pip
pip install psycopg2-binary
```

## Validar conexiónes

```python
import psycopg2

if __name__ == '__main__':
    try:
        connect = psycopg2.connect("dbname='neytor_db' user='neytor' password='neytor' host='127.0.0.1'")
        
        print('Connection established')
            
    except psycopg2.Error as e:
        print('Ha ocurrido un error: ', e)
        
    finally:
        # connect.close()
        print('Connection closed')
```

### Conexiones, registros, todo

```python
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
```

