import pymysql

if __name__ == '__main__':
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='neytor', 
                            passwd='neytor', db='neytor-db')
    
        print('Connection successful')
        
    except pymysql.MySQLError as e:
        print('Error: ', e)