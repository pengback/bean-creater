# encoding: UTF-8
import os
import this

from bean import Properties
import util
import config.mysql

class Creater:

    os.chdir(config.mysql.filepath)


    def __init__(self, bean):
        self.fileName = bean.className
        self.bean = bean
        self.fileObject = open(bean.className + '.java', 'w+')


    def createFile(self):
        self.printClass(self.bean)
        self.printProperties(self.bean.beans)
        self.printSetGetMethods(self.bean.beans)
        self.filePrinter(True, '}')

    # create bean properties
    def printProperties(self, properties):
        if(isinstance(properties, list)):
            for p in properties:
                if(isinstance(p, Properties) is False):
                    return
                sname = util.encodeCamelCase(p.name)
                self.filePrinter(True, 'private', p.dataType, sname +';')

    # create class
    def printClass(self, bean):
        self.filePrinter(True, 'class', bean.className, '{')


    def printSetGetMethods(self, properties):
        for p in properties:
            self.filePrinter(False, 'public', 'void', 'set'+p.name.title(), '(', p.dataType, '', p.name, '){')
            self.filePrinter(False, '\tthis.' + p.name, '=', p.name)
            self.filePrinter(True, '}')


    def filePrinter(self, isreturn, *args):
        s = ''
        for a in args:
            s += a + ' '
        s += '\n'
        if isreturn:
            s += '\n'
        self.fileObject.writelines(s)
