
import pymysql.cursors
import os ,time
import configparser as cparser   #读取ini文件


# ============Reading db_config.ini setting =========
# 相对取路径

base_dir = str(os.path.dirname(os.path.dirname(__file__))) #当前文件路径
# print(base_dir)
base_dir = base_dir.replace('\\','/')  #替换反斜杠（linux与window兼容）
# print(base_dir)
file_path = base_dir+'/db_config.ini' #取到文件路径
# print(file_path)


cf = cparser.ConfigParser()


cf.read(file_path)
host = cf.get('mysqlconf','host')
# print(host)
port = cf.get('mysqlconf','port')
db = cf.get('mysqlconf','db_name')
user = cf.get('mysqlconf','user')
password = cf.get('mysqlconf','password')


# ==============MySql base operating==================
class DB:

     def __init__(self):
         try:
             # Connect to the database
            self.connection = pymysql.connect(host=host,
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
         except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))

     # clear table data
     def clear(self,table_name):
         # real_sql="truncate table"+table_name+";"
         real_sql = "delete  from " + table_name + ";"
         print(real_sql)
         with self.connection.cursor() as cursor:
             cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
             cursor.execute(real_sql)
         self.connection.commit()


     # insert sql statement
     def insert(self,table_name,table_data):

         for key in table_data:
             table_data[key]="'"+str(table_data[key])+"'"
         key = ','.join(table_data.keys())
         print(key)
         value =','.join(table_data.values())
         print(value)
         real_sql = "INSERT INTO " + table_name + "(" + key + ") VALUES (" + value + ")"
         print(real_sql)

         with self.connection.cursor() as cursor:
             cursor.execute(real_sql)

         self.connection.commit()

     # close database
     def close(self):
         self.connection.close()


if __name__ == '__main__':

    db = DB()
    table_name="sign_event"
    nowtime = time.strftime("%Y-%m-%d %H_%M_%S")
    data3={'id':2,'name':'红米Pro发布会','`limit`':2000,'status':1,'address':'北京会展中心','start_time':'2017-08-20 14:00:00','create_time':nowtime}
    data ={'id': 1 , 'name': 'xiaomi' ,'`limit`':2000,'status':1,'address':'beijing','start_time':'2017-9-12 13:00:00','create_time':nowtime}
    table_name2 = "sign_guest"
    data2 ={'realname':'daisy34','phone':19232321321,'email':'dai@ee.con','sign':0,'event_id':1}

    # db.clear(table_name)
    db.insert(table_name,data3)
    db.close()
