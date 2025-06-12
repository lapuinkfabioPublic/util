import unicodedata
import string
import re

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

#curl -d "token=DAWbiMVyDhNOhBOgs7vbFMhEIUrLSQ6o2FZea=&query=" -X POST https://lapuinka.pythonanywhere.com/DoutrinaAgil/total/count/
#{"doutrinas":"501"}

@request.restful()
def count():
    response.view = 'generic.json'
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers['Access-Control-Max-Age'] = 86400
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    def GET2(*args,**vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def GET():
        uri = "mongodb://USER:PASSWORD@ds015942.mlab.com:15942/doutrina_agil"
        client = MongoClient(uri)
        db2 = client.get_default_database()
        doutrinas = db2['doutrinas']
        total = doutrinas.find().count();
        return '{"doutrinas":"' + str(total) + '"}'
    def POST(token,query):
        total  = 3
        v= "2"
        from datetime import datetime
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a = request.env.http_x_forwarded_for

        if str(token) != "DAWbiMVyDhNOhBOgs7vbFMhEIUrLSQ6o2FZea=": #Token versão DEMO
            return "Invalid Demo("+token+")"

        uri = "mongodb://USER:PASSWORD@ds015942.mlab.com:15942/doutrina_agil"
        client = MongoClient(uri)
        db2 = client.get_default_database()
        livro = 1
        query = str(remove_accents(unicode(query, "utf-8")))
        doutrinas = db2['doutrinas']
        total = doutrinas.find({'texto' : {'$regex' : '.*' + query +'.*'}}).count();

            
        return '{"doutrinas":"' + str(total) + '"}'


    return dict(GET=GET, POST=POST)
