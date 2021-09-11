import sqlite3

class sqlControler():
    def __init__(self, db_file):
        self.db_file = db_file
    
    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except EnvironmentError as e:
            print(e)
        return conn
    
    def update_ip(self, ipAddress):
        self.conn = self.create_connection()
        sql = '''
            UPDATE IP 
            SET IP_Address = (?)
            WHERE ID_IP_Address = 1
            '''
        cur = self.conn.cursor()
        cur.execute(sql, (ipAddress,))
        self.conn.commit()
        self.conn.close()
        
    def QuerySQL(self, SQL):
        self.conn = self.create_connection()
        cur = self.conn.cursor()
        cur.execute(SQL)
        res_data = cur.fetchall()
        self.conn.close()
        return res_data