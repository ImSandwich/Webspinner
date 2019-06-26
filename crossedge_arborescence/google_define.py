import urllib.request as req 

def define(term):
    request = req.urlopen("https://googledictionaryapi.eu-gb.mybluemix.net/?define="+term+"&lang=en")
    print(request.read())

define("tree")

