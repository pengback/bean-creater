# encoding: UTF-8
import mysql.connector
import bean
import creater
import config.mysql

#


try:
    cnn = mysql.connector.connect(**config.mysql.config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
cursor = cnn.cursor()
beans = []
try:
    sql_query = "select column_name as columnName, data_type, character_maximum_length from information_schema.columns where table_schema = 'test' and table_name = 'runoob_tbl';"
    cursor.execute(sql_query)
    for columnName, data_type, character_maximum_length in cursor:
        # print "%s, %s, %d\n" %(columnName, data_type, character_maximum_length)
        beans.append(bean.Properties(columnName, data_type, character_maximum_length))
        # print(columnName, data_type, character_maximum_length)

except mysql.connector.Error as e:
    print('query error!{}'.format(e))
finally:
    cursor.close()
    cnn.close()

# for b in beans:
#     creater.encodeCamelCase(b.name)

creater.printProperties(beans)

