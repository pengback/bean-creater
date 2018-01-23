# encoding: UTF-8
import util

class Properties:
    'properties class'

    def __init__(self, columnName, type, size, comment):
        self.columnName = columnName
        self.name = util.encodeCamelCase(columnName)
        self.type = type
        self.size = size
        self.dataType = util.reflectJavaDataType(type)
        self.comment = comment.encode('utf-8')

    def toString(self):
        print 'name:', self.name, ';type:', self.type, ';size:', self.size


class Bean:
    'bean class'

    def __init__(self, beans, tableName, comment):
        self.className = util.encodeCamelCase(tableName.capitalize())
        self.beans = beans
        self.tableName = tableName
        self.comment = comment.encode('utf-8')





