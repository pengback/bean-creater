# encoding: UTF-8
import util

class Properties:
    'properties class'

    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

    def toString(self):
        print 'name:', self.name, ';type:', self.type, ';size:', self.size


class Bean:
    'bean class'

    def __init__(self, beans, tableName):
        self.className = util.encodeCamelCase(tableName)
        self.beans = beans
        self.tableName = tableName






