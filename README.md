# Python DB

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