import pymysql

'''
host=None, user=None, password="",
                 database=None
'''


class SqlHelper():
    def __init__(self, host, database, user, password, ):
        self.connector = {'host': host, 'database': database, 'user': user, 'password': password};

    def __init__(self, connect_info={}):
        self.connector = connect_info;

    def exec(self, sql='',args=[]):
        db = pymysql.connect(**self.connector)
        cursor = db.cursor();
        try:
            cursor.execute(sql,args);
            db.commit();
        except:
            db.rollback();
        finally:
            db.close();

    def query(self, sql='',args=[]):
        db = pymysql.connect(**self.connector)
        cursor = db.cursor();
        try:
            cursor.execute(sql,args);
            results = cursor.fetchall();
            return results;
        except:
            db.rollback();
        finally:
            db.close();


if __name__ == '__main__':
    myconnector = {
        'host': 'localhost',
        'user': 'root',
        'password': 'insta360',
        'database': 'cnote'
    }
    SqlHelper(myconnector).exec(
        'INSERT INTO account_user(name,pwd,phone,uid) VALUES(%s,%s,%s,%s)',['cczz3', '111', '455566203', 8]);
    results = SqlHelper(myconnector).query('SELECT * FROM account_user LIMIT %s',[3]);
    for result in results:
        print(result[2]);
