from urllib.parse import parse_qs

def simple_app(environ, start_response):
    response_body = "Hello, world!\n"

    method = environ['REQUEST_METHOD']

    request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))

    if method == "GET":
        response_body += "GET parameters: \n"
        parameters = parse_qs(environ['QUERY_STRING'])
        for key, value in parameters.items():
            response_body += f"{key}: {str(value)[1:len(str(value))-1]}\n"

    if method == "POST":
        response_body += "POST parameters: \n"
        parameters = parse_qs(request_body.decode('utf-8'))
        for key, value in parameters.items():
            response_body += f"{key}: {str(value)[1:len(str(value))-1]}\n"

    response_body = response_body.encode('utf-8')

    status = '200 OK'
    headers = [('Content-type', 'text/plain'),
               ('Content-Length', str(len(response_body)))]

    start_response(status, headers)
    return [response_body]

application = simple_app