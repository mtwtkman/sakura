from io import BytesIO

from tomoyo import App, Server, resource, get, scope


def handle_get(request):
    data = ','.join(f'{k.upper()}: {v}' for k, v in request.body.items())
    return data or 'no params'


def j(request):
    return request.body or {'sakura': 'kinomoto', 'tomoyo': 'daidouji'}


def handle_post(request):
    return dict(result=True, **request.body)


@get('/decorated')
def decorated(request):
    return 'decorated'


def handle_scoped_x(request):
    return 'scoped'


def regex_path(request, id_):
    return f'id is {id_}'


app = App() \
    .service(resource('/').get(handle_get)) \
    .service(resource('/json').get(j)) \
    .service(resource('/post').post(handle_post)) \
    .service(decorated) \
    .service(
        scope('/scoped').service(resource('/x').get(handle_scoped_x))
    ) \
    .service(resource(r'/(?P<id_>\d+)').get(regex_path))
Server(app=app).bind('0.0.0.0', 55301).run()
