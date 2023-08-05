import os
import codecs
import random, string

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


def html(res, filename=None):
    if not filename:
        filename = randomword(8)
    path = os.path.dirname(os.path.dirname(__file__)) + "/data/" + filename +".html"
    print path
    with codecs.open(path,'w',encoding='utf8') as f:
        f.write(res.text)

