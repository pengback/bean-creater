# encoding: UTF-8
import re

def encodeCamelCase(str):
    str = str.encode('utf-8')
    pat = re.compile('(?P<upchar>_[A-Za-z])', re.I)
    m = pat.finditer(str)
    if m is not None:
        for r in m:
            print r.groupdict()
    else:
        print 'none group'
    result = pat.sub(encodeCamelCaseGetUpchar, str)
    return result

def encodeCamelCaseGetUpchar(m):
    d = m.groupdict()
    return d['upchar'].replace('_', '').upper()
