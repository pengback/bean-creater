# encoding: UTF-8
import re

JAVA_BASE_DATA_TYPE = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']
JAVA_REFECT_DICT = {
    'varchar': 'String',
    'datetime': 'Date'
}

def encodeCamelCase(str):
    str = str.encode('utf-8')
    pat = re.compile('(?P<upchar>_[A-Za-z])', re.I)
    m = pat.finditer(str)
    # if m is not None:
    #     for r in m:
    #         print r.groupdict()
    # else:
    #     print 'none group'
    result = pat.sub(encodeCamelCaseGetUpchar, str)
    return result

def encodeCamelCaseGetUpchar(m):
    d = m.groupdict()
    return d['upchar'].replace('_', '').upper()


def reflectJavaDataType(str):
    str = str.encode('utf-8')
    if str in JAVA_BASE_DATA_TYPE:
        return str
    if str in JAVA_REFECT_DICT:
        return JAVA_REFECT_DICT.get(str)
    else:
        return str.title()