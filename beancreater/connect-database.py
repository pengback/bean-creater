# encoding: UTF-8
import mysql.connector
from beancreater import bean
from beancreater.creater import Creater
import config.mysql

#


try:
    cnn = mysql.connector.connect(**config.mysql.config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
cursor = cnn.cursor()

data_base = config.mysql.config.get('database')

creater_array = []

try:
    for table in config.mysql.tables_name:
        beans = []
        param = (data_base, table)
        sql_query = "select table_name, table_comment from information_schema.tables  where table_schema = %s and table_name = %s;"
        cursor.execute(sql_query, param)
        table_result = cursor.fetchone()
        if table_result:

            sql_query = "select column_name as columnName, data_type, character_maximum_length, column_comment from information_schema.columns " \
                        "where table_schema = %s and table_name = %s ;"
            print 'table is: ', table

            cursor.execute(sql_query, param)
            result = cursor.fetchall()
            for columnName, data_type, character_maximum_length, column_comment in result:
                beans.append(bean.Properties(columnName, data_type, character_maximum_length, column_comment))

            b = bean.Bean(beans, table, table_result[1])
            creater = Creater(b)
            creater.createFile()
            creater_array.append(creater)

except mysql.connector.Error as e:
    print('query error!{}'.format(e))
finally:
    cursor.close()
    cnn.close()



