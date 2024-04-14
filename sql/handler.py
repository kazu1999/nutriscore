import mysql.connector

class db:
    def connect(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="kazuto",
            password="kazuto7171",
            database="nutriscore"
        )
        self.conn = conn
        self.cursor = conn.cursor(buffered=True)
    
    def getDb(self):
        if self.cursor==None:
            self.connect()
        return self.cursor
    
    def insertId(self,email_address, password):
        # TODO 同じemail_addressは入れない
        print(self.cursor)
        self.cursor.execute("INSERT INTO id VALUES (DEFAULT, %s, %s ,DEFAULT)", (email_address, password))
        self.conn.commit()
    
    def selectId(self, email_address):
        self.cursor.execute("SELECT * FROM id WHERE mail_address=%s", (email_address, ))
        return self.cursor.fetchone()
    
    def deleteId(self, email_address):
        self.cursor.execute('DELETE FROM id WHERE mail_address=%s',(email_address,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
    

    def insertRecord(self,calories, fat, protein, carbohydrates, indivi_id=1):
        self.cursor.execute("INSERT INTO record VALUES (DEFAULT, %s, %s ,%s, %s ,%s,DEFAULT)", (str(indivi_id), calories, fat, protein, carbohydrates))
        self.conn.commit()
    
    def selectRecord(self, indivi_id=1):
        self.cursor.execute("SELECT * FROM record WHERE indivi_id=%s", (str(indivi_id), ))
        selected = self.cursor.fetchall()
        nutri_dict={}
        nutri_dict['time']=[]
        nutri_dict['calories']=[]
        nutri_dict['fat']=[]
        nutri_dict['protein']=[]
        nutri_dict['carbohydrates']=[]
        for i in range(len(selected)):
            nutri_dict['calories'].append(selected[i][2])
            nutri_dict['fat'].append(selected[i][3])
            nutri_dict['protein'].append(selected[i][4])
            nutri_dict['carbohydrates'].append(selected[i][5])
            recordtime = selected[i][6]
            recordtime_str = recordtime.strftime('%Y-%m-%d %H:%M:%S')
            nutri_dict['time'].append(recordtime_str)
        return nutri_dict
    
    def deleteRecord(self, indivi_id=1):
        self.cursor.execute('DELETE FROM record WHERE indivi_id=%s',(str(indivi_id),))
        self.conn.commit()


def main():
    db_instance = db()
    db_instance.connect()
    '''
    
    print('insertId test')
    db_instance.insertId('squid.7171@gmail.com','kazuto7171')
    

    print('selectId test')
    selected = db_instance.selectId('squid.7171@gmail.com')
    print(type(selected[0]))
    print(selected[0])

    print('deleteId test')
    db_instance.deleteId('squid.7171@gmail.com')


    print('insertRecord test')
    db_instance.insertRecord('2','3','4','5','1')
    '''

    print('selectRecord test')
    nutri_dict = db_instance.selectRecord(40)
    print(nutri_dict)
    



    '''

    print('deleteRecord test')
    db_instance.deleteRecord('1')
    '''

    db_instance.close()



if __name__ =='__main__':
    main()

        
