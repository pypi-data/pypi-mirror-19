# This file was auto-generated. Do not manually edit or save. What are you doing looking at it? Close it now!
# Generated on 2016-06-30 11:19:12.605000
#
import base64
import StringIO

def getsome(item, filelike=True):
    data = _contents[item]
    data = base64.b64decode(data)
    if filelike:
        data = StringIO.StringIO(data)
    return data

_contents = {
}
