# encoding: UTF-8
import os
import time
from bean import Properties
import config.mysql


EXTENDS_PROPERTIES = ['id', 'corp_id', 'createdBy', 'createdOrg', 'createdDate', 'lastModifiedBy', 'lastModifiedOrg', 'lastModifiedDate', 'optlock']

class Creater:

    os.chdir(config.mysql.filepath)


    def __init__(self, bean):
        self.fileName = bean.className
        self.bean = bean
        self.fileObject = open(bean.className + '.java', 'w+')
        self.tab_num = 0;

    def addTabNum(self):
        self.tab_num += 1

    def subTabNum(self):
        self.tab_num -= 1


    def createFile(self):
        self.printClass(self.bean)
        self.addTabNum()
        self.printProperties(self.bean.beans)
        self.printSetGetMethods(self.bean.beans)
        self.subTabNum()
        self.filePrinter(True, '}')

    # create bean properties
    def printProperties(self, properties):
        if(isinstance(properties, list)):
            for p in properties:
                if(isinstance(p, Properties) is False):
                    return

                if p.columnName in EXTENDS_PROPERTIES:
                    continue

                self.filePrinter(False, '@MetaData(value=\"' + p.comment + '\")')
                print p.size
                if p.size != None:
                    self.filePrinter(False, '@Column(name=\"'+ p.columnName +'\", length='+str(p.size)+')')
                else:
                    self.filePrinter(False, '@Column(name=\"' + p.columnName + '\")')
                self.filePrinter(True, 'private', p.dataType, p.name +';')

    # create class
    def printClass(self, bean):
        self.filePrinter(False, '/**')
        self.filePrinter(False, ' * @desc', bean.comment)
        self.filePrinter(False, ' * @create', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
        self.filePrinter(False, ' **/')
        self.filePrinter(False, '@MetaData(value = "' + bean.comment + '")')
        self.filePrinter(False, '@Entity(name = "' + bean.className + '")')
        self.filePrinter(False, '@Table(name = "' + bean.tableName + '", uniqueConstraints = { @UniqueConstraint(columnNames = "id") })')
        self.filePrinter(True, 'class', bean.className, 'extends BaseCorpEntity {')


    def printSetGetMethods(self, properties):
        for p in properties:
            self.filePrinter(False, 'public', 'void', 'set'+p.name.title()+'('+p.dataType,  p.name+'){')
            self.filePrinter(False, '\tthis.' + p.name, '=', p.name)
            self.filePrinter(True, '}')

            self.filePrinter(False, 'public', p.dataType, 'get' + p.name.title()+'(){')
            self.filePrinter(False, '\treturn ' + p.name)
            self.filePrinter(True, '}')


    def filePrinter(self, isreturn, *args):
        s = ''
        i = 0
        while i < self.tab_num:
            s += '\t'
            i += 1
        for a in args:
            s += a + ' '
        s += '\n'
        if isreturn:
            s += '\n'
        self.fileObject.writelines(s)
