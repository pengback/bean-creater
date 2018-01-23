# encoding: UTF-8
import os
import time
from bean import Properties
import config.mysql



class Creater:

    os.chdir(config.mysql.filepath)


    def __init__(self, bean):
        os.chdir(config.mysql.filepath)
        self.fileName = bean.className
        self.bean = bean
        self.fileObject = None
        self.tab_num = 0
        if os.path.exists(bean.className) == False:
            os.mkdir(bean.className)
        os.chdir(bean.className)

    def addTabNum(self):
        self.tab_num += 1

    def subTabNum(self):
        self.tab_num -= 1


    def createFile(self):
        self.fileObject = open(self.bean.className + '.java', 'w+')
        self.printClass(self.bean)
        self.addTabNum()
        self.printProperties(self.bean.beans)
        self.printSetGetMethods(self.bean.beans)
        self.subTabNum()
        self.filePrinter(True, '}')
        self.fileObject = None

    # create bean properties
    def printProperties(self, properties):
        if(isinstance(properties, list)):
            for p in properties:
                if(isinstance(p, Properties) is False):
                    return

                if p.columnName in config.mysql.EXTENDS_PROPERTIES:
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
        self.filePrinter(True, 'class', bean.className, 'extends', self.getExtendsClass('entity'), '{')


    def printSetGetMethods(self, properties):
        for p in properties:
            self.filePrinter(False, 'public', 'void', 'set'+p.name.title()+'('+p.dataType,  p.name+'){')
            self.filePrinter(False, '\tthis.' + p.name, '=', p.name)
            self.filePrinter(True, '}')

            self.filePrinter(False, 'public', p.dataType, 'get' + p.name.title()+'(){')
            self.filePrinter(False, '\treturn ' + p.name)
            self.filePrinter(True, '}')


    def filePrinter(self, isreturn, *args):
        if self.fileObject == None:
            return
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


    def createController(self):
        cName = self.getFileName('controller')
        self.fileObject = open(cName+'.java', 'w+')

        self.filePrinter(True, 'package', config.mysql.PACKAGE_BASE_PATH + '.web.controller')
        self.filePrinter(False, '/**')
        self.filePrinter(False, ' * @desc', self.bean.comment + ' Controller')
        self.filePrinter(False, ' * @create', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.filePrinter(False, ' **/')
        self.filePrinter(False, '@Controller')
        self.filePrinter(False, '@RequestMapping(value = "")')

        swap = ['public', 'class', cName]
        if self.getExtendsClass('controller'):
            swap.append('extends')
            swap.append(self.getExtendsClass('controller'))
        swap.append('{')
        self.filePrinter(True, *swap)
        self.addTabNum()
        self.filePrinter(True, 'private final Logger LOGGER = LoggerFactory.getLogger('+cName+'.class);')

        self.filePrinter(False, '@Autowired')
        self.filePrinter(True, 'private', self.getFileName('service'), self.getFileName('service'), ';')

        self.filePrinter(False, '@Override')
        self.filePrinter(False, 'protected BaseService<'+self.bean.className+', String> getEntityService() {')
        self.addTabNum()
        self.filePrinter(False, 'return reportInfoService;')
        self.subTabNum()
        self.filePrinter(True, '}')

        self.filePrinter(False, '/**')
        self.filePrinter(False, ' * 初始化数据')
        self.filePrinter(False, ' *')
        self.filePrinter(False, ' * @param request')
        self.filePrinter(False, ' * @param model')
        self.filePrinter(False, ' * @param id')
        self.filePrinter(False, ' */')
        self.filePrinter(False, '@ModelAttribute')
        self.filePrinter(False, 'public void prepareModel(HttpServletRequest request, Model model, @RequestParam(value = "id", required = false) String id) {')
        self.addTabNum()
        self.filePrinter(False, 'super.initPrepareModel(request, model, id);')
        self.subTabNum()
        self.filePrinter(True, '}')



        self.subTabNum()
        self.filePrinter(True, '}')
        self.fileObject = None


    def getExtendsClass(self, type):
        if type in config.mysql.EXTENDS_CLASS:
            return config.mysql.EXTENDS_CLASS.get(type).replace('$bean_name$', self.bean.className)
        else:
            return None

    def getFileName(self, type):
        if type == 'controller':
            return self.bean.className + 'Controller'
        elif type == 'service':
            return self.bean.className + 'Service'
        elif type == 'dao':
            return self.bean.className + 'Dao'
        else:
            return self.bean.className


