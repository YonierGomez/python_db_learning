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