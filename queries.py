import pymysql
import datetime
import re

class sql_queries(object):
    def __init__ (self):
        
        host = "localhost"
        user = "Sujay"
        password = "laferrar1"
        db = "mydatabase"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    
    def insert_preview(self, filename):
        sql = 'insert into preview(ID, FILE_NAME, DATE_TIME) values (%s, %s, %s)'
        ts = datetime.datetime.now() 
        val = (0, filename, ts)
        self.cur.execute(sql, val)
        self.con.commit()
        return
    
    def insert_listb(self, ord_num, cust_name, ret_name, ord_date, bill_add):
        date = re.split("\.", ord_date)
        DD = date[0]
        MM = date[1]
        YYYY = date[2]
        ord_date = YYYY+'-'+MM+'-'+DD
        sql = 'insert into listb(ord_num, cust_name, ret_name, ord_date, bill_add) values (%s, %s, %s, %s, %s)'
        val = (ord_num, cust_name, ret_name, ord_date, bill_add)
        self.cur.execute(sql, val)
        self.con.commit()
        return
    
    def delete_preview(self, id):
        sql = 'delete from preview where ID = %s'
        val = (id, )
        self.cur.execute(sql, val)
        self.con.commit()
        
    def get_filename(self, id):
        sql = 'select file_name from preview where id = %s'
        val = (id, )
        self.cur.execute(sql, val)
        result = self.cur.fetchone()
        x = result['file_name']
        return x