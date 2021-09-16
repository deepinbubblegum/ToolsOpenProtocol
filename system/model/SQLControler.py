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
    
    def db_Update_ip(self, ipAddress):
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
        
    def db_QuerySQL(self, SQL):
        self.conn = self.create_connection()
        cur = self.conn.cursor()
        cur.execute(SQL)
        res_data = cur.fetchall()
        self.conn.close()
        return res_data
    
    def db_del_step(self, ID_STEP, ID_Link_step):
        self.conn = self.create_connection()
        sql = '''
            DELETE FROM Step
            WHERE ID_STEP = (?)
            AND ID_Link_step = (?)
            '''
        cur = self.conn.cursor()
        cur.execute(sql, (ID_STEP, ID_Link_step,))
        self.conn.commit()
        self.conn.close()
        
    def db_add_step(self, stepTRAY, stepSocket, stepTools, stepLink_ID):
        self.conn = self.create_connection()
        sql = '''
            INSERT INTO Step (ID_STEP, ID_Link_step, Step_number, Socket_ID_Step, ID_TRAY_ID, Step_Tools_ID) 
            VALUES((
                    SELECT IFNULL(MAX(ID_STEP), 0) + 1
                    FROM Step
                    ORDER BY ID_STEP
                ), (?),
                (
                    SELECT IFNULL(MAX(Step_number), 0) + 1
                    FROM Step 
                    WHERE ID_Link_step = (?)
                    ORDER BY Step_number
                ), 
            (?), (?), (?))
        '''
        cur = self.conn.cursor()
        cur.execute(sql, (stepLink_ID, stepLink_ID, stepSocket, stepTRAY, stepTools))
        self.conn.commit()
        self.conn.close()