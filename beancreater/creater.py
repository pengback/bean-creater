# encoding: UTF-8
from bean import Properties
import util

# create bean properties
def printProperties(properties):
    if(isinstance(properties, list)):
        for p in properties:
            if(isinstance(p, Properties) is False):
                return
            sname = util.encodeCamelCase(p.name)
            filePrinter('private', p.type.title(), sname, ';')

# create class
def printClass(bean):
    filePrinter('class', bean.className, '{')


# create class file name




def filePrinter(*args):
    print args
