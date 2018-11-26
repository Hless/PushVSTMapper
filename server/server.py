from bottle import route, run, response
from json import dumps


def json_response(value):
    response.content_type = 'application/json'
    return value

@route('/configs')
def index():
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
